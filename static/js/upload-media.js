
window.onload = ()=>{

    const main_url = window.location.protocol + '//' + window.location.host;
    console.log(main_url);
    // const admin_url = main_url + '/admin2/';
    // const controller_url = admin_url + 'app/controllers/';
    
    document.addEventListener('click', event=>{
        let element = event.target;

        if(element.id == "upload-media"){
            // validate_form();
            let upload_form = document.getElementById("media-form");
            formSubmit(upload_form);
        }
    });

    function formSubmit(upload_form){

        let media_input_ele = document.getElementById('media-file');
        let media_file = media_input_ele.files[0];
        let formData = new FormData();
        formData.append('media_file', media_file);
        formData.append('action', 'upload');

        document.getElementById('status-window').innerHTML = '';
        document.getElementById('error-window').innerHTML = '';

        //
        if(media_file==undefined || media_file.size == 0){
            document.getElementById('error-window').innerHTML = 'No file selected';
            return false;
        }
        if(media_file.size > 5000000){
            document.getElementById('error-window').innerHTML = 'File size greater than 5MB!';
            return false;
        }

        
        // const endpoint = upload_form.dataset.url;
        const endpoint = '/upload_media';
        // const endpoint = `${window.origin}/upload_media`;
        // const endpoint = `${window.location}/upload_media`;

        const options = {
            // method: 'POST',
            method: (upload_form.method) ? upload_form.method : 'POST',
            // headers:{
            //     'Content-Type': 'application/json',
            // },
            body: formData
        };

        fetch(endpoint, options)
            .then(response =>{
                console.log(response);
                if(response.ok){
                    console.log("connected with server..");
                    return response.json();
                    // return response.text();
                }
                else alert("Unable to submit form. Try again later.");
            })
            .then(data =>{
                console.log(data);
                document.getElementById('status-window').innerHTML = data.message;
            })
            .catch(error =>{
                console.log('Something went wrong.', error);
                document.getElementById('error-window').innerHTML = error;
            });
    }
};