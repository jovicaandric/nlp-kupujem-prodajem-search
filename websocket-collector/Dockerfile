FROM openjdk:12.0.1

RUN mkdir /app
COPY build/libs/*.jar /app/app.jar
COPY scripts/run.sh /app
COPY build/resources/main/application.yml /app/application.yml
RUN chmod u+x /app/run.sh
WORKDIR /app

ENTRYPOINT ["/app/run.sh"]
