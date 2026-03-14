# Build stage for Go
FROM --platform=linux/amd64 golang:1.26-alpine AS builder

RUN apk add --no-cache gcc musl-dev

WORKDIR /app

COPY go-llm-gateway/go.mod go-llm-gateway/go.sum ./
RUN go mod download

COPY go-llm-gateway/ ./

RUN CGO_ENABLED=0 go build -o gateway ./cmd/gateway

# Runtime stage
FROM alpine:latest

RUN apk add --no-cache ca-certificates

WORKDIR /app

COPY --from=builder /app/gateway /usr/local/bin/
COPY --from=builder /app/configs/ /app/configs/

ENV APP_SERVER_PORT=:8080
ENV APP_LOGGING_LEVEL=info

EXPOSE 8080

ENTRYPOINT ["gateway"]
