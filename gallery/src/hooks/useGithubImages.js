import {useState, useEffect} from 'react'
import imageLocations from '../image-locations.json'
import axios from 'axios'

/*
author: Anthony D'Alesandro

hook with the sole purposes of extracting data out of use given image-locations.json file and grabbing that data from github.
*/
function useGithubImages() {
    const [images, setImages] = useState([]);
    useEffect(() => {
        async function onLoad() {
            for(let i = 0; i < imageLocations.locations.length; i++) {
                const location = imageLocations.locations[i];
                const headers = {
                    'X-GitHub-Api-Version': '2022-11-28',
                    'Accept': 'application/vnd.github.html+json'
                }
                const PATH = location.folderPath;
                const REPO = location.repo;
                const OWNER = location.owner;
                const response = await axios.get(`https://api.github.com/repos/${OWNER}/${REPO}/contents/${PATH}`, {headers});
                setImages(response.data.filter(item => item.type=='file' && (item.name.endsWith('.jpg') || item.name.endsWith('.png') || item.name.endsWith('.jpeg') || item.name.endsWith('.gif'))));
            }

            // const octokit = new Octokit({
            //     auth: process.env.REACT_APP_GITHUB_ACCESS_TOKEN
            // });
            // for(let i = 0; i < imageLocations.locations.length; i++) {
            //     const location = imageLocations.locations[i];
            //     const response = await octokit.request('GET /repos/{owner}/{repo}/contents/{path}', {
            //         owner: location.owner,
            //         repo: location.repo,
            //         path: location.folderPath,
            //         headers: {
            //         'X-GitHub-Api-Version': '2022-11-28'
            //         }
            //     })
            //     const imageArr = response.data;
            //     setImages(prev => prev.concat(imageArr));
            // }
        }
        onLoad();
    },[])
    return images;
}

export default useGithubImages