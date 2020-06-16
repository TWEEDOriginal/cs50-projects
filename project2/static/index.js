document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#submit').disabled = true;
    
    document.querySelector('#display_name').onkeyup = () => {
                    if (document.querySelector('#display_name').value.length > 0)
                        document.querySelector('#submit').disabled = false;
                    else
                        document.querySelector('#submit').disabled = true;
                };
        

});
