# model-earth-image-gallery
author: Anthony D'Alesandro  
  
model-earth-image-gallery is a react built application that makes a request to a specific github repo and renders all the images stored at that repository.

# Config / Setup
### ./image-gallery/.env file
this file is expected to have the access token needed to access any private repository or complete any action that requires authentication. May be omitted in some cases.
```env
REACT_APP_GITHUB_ACCESS_TOKEN=""
```

### configure github image folder endpoint file
./image-gallery/src/image-locations.json  
```json
{
    "locations": [
        {
            "owner": "ModelEarth",
            "repo": "replicate",
            "folderPath": "/images"
        },
        {
            "owner": "Tonyy456",
            "repo": "replicate",
            "folderPath": "/images"
        }
    ]
}
```

# Running the Application
install the application
```sh
npm i
```

start the server
```sh
npm run start
```

# Build for development
has a known issue! octokit may or maynot fail to build.
```sh
npm run build
```
