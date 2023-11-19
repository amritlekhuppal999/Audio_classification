
window.onload = ()=>{
    
    document.addEventListener('click', event=>{
        let element = event.target;

        if(element.id == "upload-media"){
            // validate_form();
            if(validate_form()){
                // alert("Media Sent");
                let upload_form = document.getElementById("media-form");
                formSubmit(upload_form);
            }
        }
    });

    function validate_form(){
        let media_input_ele = document.getElementById('media-file');

        if(media_input_ele.files.length){
            let media_file = media_input_ele.files[0];
            alert(media_file.name);
        }
        else {
            alert("Select your audio file.");
            return false;
        }

        return true;
    }

    function formSubmit(upload_form){

        let media_input_ele = document.getElementById('media-file');
        const formData = new FormData();
        formData.append('media_file', media_input_ele.files[0]);
        
        const endpoint = upload_form.dataset.url;

        const options = {
            method: (upload_form.method) ? upload_form.method : 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: formData
        };

        fetch(endpoint, options)
            .then(response =>{
                if(response.ok){
                    // console.log(response.json());
                    alert("things went well.. here is your data");
                }
                else alert("Unable to submit form. Try again later.");
            })
            // .then(data =>{})
            .catch(error =>{
                console.log('Something went wrong.', error);
            });
    }
};