
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

        document.getElementById('upload-media').disabled = true;

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
            document.getElementById('upload-media').disabled = false;
            return false;
        }
        if(media_file.size > 5000000){
            document.getElementById('error-window').innerHTML = 'File size greater than 5MB!';
            document.getElementById('upload-media').disabled = false;
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
                document.getElementById('upload-media').disabled = false;
            })
            .then(data =>{
                console.log(data);
                img_charts = document.getElementById('image-charts');

                let bar_chart_img = document.createElement('img');
                bar_chart_img.src = data.plot_urls.bar_chart;

                let waveform_img = document.createElement('img');
                waveform_img.src = data.plot_urls.wave_chart;

                let spectrogram_img = document.createElement('img');
                spectrogram_img.src = data.plot_urls.spectrogram;

                let graph_img = document.createElement('img');
                graph_img.src = data.plot_urls.graph;

                img_charts.appendChild(bar_chart_img);
                img_charts.appendChild(waveform_img);
                img_charts.appendChild(spectrogram_img);
                img_charts.appendChild(graph_img);

                document.getElementById('status-window').innerHTML = `
                    <h3>${data.message}</h3>
                    <h3>${data.Sample_rate}</h3>
                    <h3>${data.duration}</h3>
                    <h3>${data.size}</h3>
                    <h3>${data.string1}</h3>
                `;
            })
            .catch(error =>{
                console.log('Something went wrong.', error);
                document.getElementById('error-window').innerHTML = error;
                document.getElementById('upload-media').disabled = false;
            });
    }
};