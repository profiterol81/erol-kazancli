FROM golang:alpine
RUN apk add --no-cache git
RUN apk add --no-cache sqlite-libs sqlite-dev
RUN apk add --no-cache build-base

WORKDIR /go/src/bidtracking/
ADD ./src/bidtracking/* /go/src/bidtracking/
RUN go get -d -v
RUN go build -o bidtracking

WORKDIR /app
RUN cp /go/src/bidtracking/bidtracking /app
ADD ./src/bidtracking/config.json /app
EXPOSE 8000

CMD [ "./bidtracking" ]