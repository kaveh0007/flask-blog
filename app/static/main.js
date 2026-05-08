function handleDelete(postId){
    fetch('/post/delete', {
        method: "POST",
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify({postId}) // Convert JS object to JSON string
    })
    .then((response)=>{
        return response.json()}) // Parsing the response from Flask
    .then((jsonResponse)=>{
        if(jsonResponse){
            window.location.href = jsonResponse.redirect_url
        }
    })
    .catch((error) => {console.error("error: "+error)})
}