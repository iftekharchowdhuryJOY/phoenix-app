# 1. Base Image: The official Tomcat (Java) server
FROM tomcat:9-jdk17

# 2. The Fix: Unpack the default "Welcome" app
# We delete the empty 'webapps' folder and rename the backup folder to 'webapps'
RUN rm -rf webapps && mv webapps.dist webapps

# 3. Documentation: Tell the world this app listens on 8080
EXPOSE 8080

# 4. Startup Command: Run Tomcat
CMD ["catalina.sh", "run"]