@echo off

REM ===============================================
REM MongoDB cleanup before build (רק כש-MongoDB דולק)
REM ===============================================
REM echo ===== MongoDB cleanup before build =====
REM docker exec -it mongodb mongosh processed_tweets --eval "db.tweets.drop(); db.tweets-antisemitic.drop(); db.tweets-not-antisemitic.drop();"

echo.
echo ===== Building all apps images with Docker-compose =====
docker-compose --build

echo.
echo ===== Connecting to Docker Hub =====
docker login

echo.
echo ===== Tagging each app =====
docker tag feature_text_malicious-fetch_tweets_atlas shuki120/fetch-tweets-atlas:latest
docker tag feature_text_malicious-preprocess shuki120/preprocess:latest
docker tag feature_text_malicious-enricher shuki120/enricher:latest
docker tag feature_text_malicious-persister shuki120/persister:latest
docker tag feature_text_malicious-data_retrieval shuki120/data-retrieval:latest

echo.
echo ===== Pushing all apps to Docker Hub =====
docker push shuki120/fetch-tweets-atlas:latest
docker push shuki120/preprocess:latest
docker push shuki120/enricher:latest
docker push shuki120/persister:latest
docker push shuki120/data-retrieval:latest

echo.
echo ====== Starting deployment on Google Cloud ======

REM נכנס לתיקיית infra
cd infra

REM עובר על כל התיקיות שבתוך infra ומיישם kubectl apply
for /D %%F in (*) do (
    echo.
    echo ====== Deploying %%F ======
    kubectl apply -f %%F/
)

echo.
echo ====== Deployment finished ======
pause
