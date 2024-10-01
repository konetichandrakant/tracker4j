## Upload Resume Setup 

<ol>
  <li> First go into the profile section <br>
  cd src/components/profile
  </li>
  <br>
  <li> Then install the necesseary node dependecies<br>
    npm install googleapis multer expresss
  </li>
  <br>
  <li>
    set the path to your resume folder on line no 119 of app.js (as node cant access the whole of the system for security reasons)
    "${setpath}"+fileObject.originalname
  </li>
  <br>
  <li> To start the api <br>
    node app.js
  </li>
    
</ol>
