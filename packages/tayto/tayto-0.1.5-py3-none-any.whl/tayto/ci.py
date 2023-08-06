from tayto import linux


def react_push(src:str) -> None:
  linux.bash(f'''
docker rm -f c-react
docker image rm -f quangdaicaa/react:current
cd {src}
npm install
npm run build --omit=dev
cat > Dockerfile << EOF
FROM quangdaicaa/react:alpine
ADD build /code
EOF
docker build -t quangdaicaa/react:current .
cd ~
docker push quangdaicaa/react:current
docker run -d -p 80:3000 --name c-react quangdaicaa/react:current
''')