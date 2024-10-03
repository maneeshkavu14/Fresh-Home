
      function get_id(id) {
        console.log(id)
        sessionStorage.setItem('key', id);
      }


      function send_reply() {
        console.log('re')
        console.log(document.getElementById('reply').value)

        var dt = {
          complaint_id: sessionStorage.getItem('key'),
          reply: document.getElementById('reply').value
        }


        fetch("http://localhost:5000/admin_reply_complaints", {
          method: "POST",
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dt)
        }).then(res => {
          console.log("Request complete! response:", res);
        });


      }
