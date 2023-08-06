from bottlenest import NestFactory
from bottlenest.transports.http import HttpTransport
from .app.AppModule import AppModule


def main():
    app = NestFactory.createMicroservice(
        AppModule,
        transport=HttpTransport(port=3000),
    )

    app.listen()


if __name__ == '__main__':
    main()
