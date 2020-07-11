FROM openjdk:8-jre-alpine

RUN mkdir /app
COPY build/libs/*.jar /app/app.jar
COPY build/resources/main/application.yml /app/application.yml
WORKDIR /app
RUN chmod +x app.jar

ENTRYPOINT java -jar app.jar
