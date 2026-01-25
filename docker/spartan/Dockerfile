# 1. Base Image: The official .NET sample (The one that works)
FROM mcr.microsoft.com/dotnet/samples:aspnetapp

# 2. Configuration: We explicitely expose 8080 (Good for documentation)
EXPOSE 8080

# 3. Environment: Ensure it listens on all interfaces (0.0.0.0)
ENV ASPNETCORE_URLS=http://+:8080