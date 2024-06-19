# ChatIAMs

LLM+climate models

![screenshoot](https://github.com/yl1127/ChatIAMs/blob/main/Web_screenshot.png)

## Running with docker

### Build and run container with the latest code

You should have the following packages installed:

- git
- wget
- docker

As long as you have them, do:

```bash
git clone https://github.com/yl1127/ChatIAMs.git
docker build -t chatiams .
docker run -p 8501:8501 chatiams
```

Then open `http://localhost:8501/` in your browser.
