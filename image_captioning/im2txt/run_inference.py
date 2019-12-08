# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Generate captions for images using default beam search parameters."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import urllib
import multiprocessing as mp

import tensorflow as tf
from PIL import Image

from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("checkpoint_path", "",
                       "Model checkpoint file or directory containing a "
                       "model checkpoint file.")
tf.flags.DEFINE_string("vocab_file", "", "Text file containing the vocabulary.")
tf.flags.DEFINE_string("input_image_urls", "",
                       "File pattern or comma-separated list of file patterns "
                       "of image files.")

tf.logging.set_verbosity(tf.logging.INFO)

CAPTIONS_DIR = './captions_new'

def worker(image_urls):
  # Build the inference graph.
  g = tf.Graph()
  with g.as_default():
    model = inference_wrapper.InferenceWrapper()
    restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
                                               FLAGS.checkpoint_path)
  g.finalize()

  # Create the vocabulary.
  vocab = vocabulary.Vocabulary(FLAGS.vocab_file)

  tf.logging.info("Running caption generation on given image URLs")

  with tf.Session(graph=g) as sess:
    # Load the model from checkpoint.
    restore_fn(sess)

    # Prepare the caption generator. Here we are implicitly using the default
    # beam search parameters. See caption_generator.py for a description of the
    # available beam search parameters.
    generator = caption_generator.CaptionGenerator(model, vocab)

    if not os.path.exists(CAPTIONS_DIR):
      os.makedirs(CAPTIONS_DIR) 

    num_failed = 0
    for num_images_captioned, url in enumerate(image_urls):
      if not url:
        print("ERROR: URL is empty.")
        num_failed += 1
        continue

      url = url.strip()

      try:
        img_filename = 'image_tmp_%' % url.split('/')[-1]
        urllib.urlretrieve(url, img_filename)
      except:
        print("ERROR: Image download failed.")
        num_failed += 1
        continue

      with tf.gfile.GFile(img_filename, "rb") as f:
        image = f.read()

      try:
        captions = generator.beam_search(sess, image)
        final_caption = None
        print("(%d / %d) Captions for image %s:" % (num_images_captioned, len(image_urls), url))
        for i, caption in enumerate(captions):
          # Ignore begin and end words.
          sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]
          sentence = " ".join(sentence)

          if i == 0:
            final_caption = sentence

          print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))
      except:
        print("ERROR: Generating captions failed.")
        num_failed += 1
        continue

      # save caption
      if not final_caption:
        print("ERROR: Generating captions failed.")
        num_failed += 1
        continue

      out_filename = url.split('/')[-1] + '.txt'
      with open(os.path.join(CAPTIONS_DIR, out_filename), 'w') as f:
        f.write(final_caption)

      # clean up downloaded image
      os.remove(img_filename)

    print("Num Failed: %d / %d" % (num_failed, len(image_urls)))


def main(_):
  image_urls = None
  with open(FLAGS.input_image_urls, "r") as f:
    image_urls = f.readlines()
  
  chunk_size = int(math.ceil(len(image_urls) / float(mp.cpu_count())))
  print("Chunk Size: %d" % chunk_size)
 
  chunks = [image_urls[x:x+chunk_size] for x in xrange(0, len(image_urls), chunk_size)]
  with Pool(processes=mp.cpu_count()) as p:
    p.map(worker, chunks)

if __name__ == "__main__":
  tf.app.run()
