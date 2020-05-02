FROM openjdk:12.0.1

RUN mkdir /app
COPY build/libs/*.jar /app/app.jar
COPY build/resources/main/application.yml /app/application.yml
WORKDIR /app

ENTRYPOINT ["java -jar app.jar"]
