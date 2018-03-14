# Adapted from https://github.com/supergiant/supergiant/blob/master/build/Dockerfile.build
FROM golang:1-stretch

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        jq \
    && rm -rf /var/lib/apt/lists/*

RUN go get -u github.com/jteeuwen/go-bindata/... \
    && go get -u github.com/kardianos/govendor

WORKDIR /go/src/github.com/supergiant/supergiant

COPY config /go/src/github.com/supergiant/supergiant/config
COPY ui /go/src/github.com/supergiant/supergiant/ui
RUN go-bindata -pkg bindata -o bindata/bindata.go config/providers/... ui/assets/... ui/views/...

COPY cmd /go/src/github.com/supergiant/supergiant/cmd
COPY pkg /go/src/github.com/supergiant/supergiant/pkg
COPY test /go/src/github.com/supergiant/supergiant/test
COPY vendor /go/src/github.com/supergiant/supergiant/vendor
RUN CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build -a -o dist/bin/supergiant -ldflags '-extldflags "-static"' ./cmd/server

CMD ["ash"]
