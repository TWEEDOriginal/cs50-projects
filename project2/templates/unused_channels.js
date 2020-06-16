
    <script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.0.11/handlebars.min.js"></script>
        
        <script>

<script id="channels" type="text/template">
           
                {% raw -%}
                 <li>
                 <a href ="#"> 
                  {{ value }}
                       </a>
                      </li>
                {%- endraw %}
            
        </script>
  <script>

           
            document.addEventListener('DOMContentLoaded', () => {
                document.querySelector('#create').onclick = ()  => {

                   const request = new XMLHttpRequest();
                    const channel = document.querySelector('#channel').value;
                    request.open('POST', '/channels');
                 
        const data = new FormData();
        data.append('channel', channel);

        // Send request
        request.send(data);
        return false;
                };
            });
        </script>
 // Template for roll results
            const template = Handlebars.compile(document.querySelector('#channels').innerHTML);
   request.onload = () => {
                     const data = JSON.parse(request.responseText);

                    // Add roll results to DOM.
                    const content = template({'values': data.channels_created});
                   
                }

 document.querySelector('#list_of_channels').innerHTML += content;