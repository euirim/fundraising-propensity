docker build -t image_captioning .
docker run --rm -v $(pwd):/app -it image_captioning /bin/bash
