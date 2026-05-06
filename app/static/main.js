function handle_search(){
    let author = document.getElementById("search").value
    fetch('/process', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json' // Tell the server we are sending JSON
    },
    body: JSON.stringify({author}) // Convert JS object to JSON string
    })
    .then(response => response.json()) //Parsing the response from Flask (jQuery $.ajax did it implicitly)
    .then(jsonResponse => {
        if(jsonResponse){
            window.location.href=jsonResponse.redirect_url
        }
    })
    .catch(error => console.error("Error sending data:", error))
}

function handleDelete(postId){
    fetch('/post/delete', {
        method: "POST",
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify({postId})
    })
    .then((response)=>{
        return response.json()})
    .then((jsonResponse)=>{
        if(jsonResponse){
            window.location.href = jsonResponse.redirect_url
        }
    })
    .catch((error) => {console.error("error: "+error)})
}