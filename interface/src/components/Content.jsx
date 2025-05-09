import { useState } from "react";
import Zoom from 'react-medium-image-zoom';
import 'react-medium-image-zoom/dist/styles.css';
import "./content.css";
function Content() {
  const [paragraph, setParagraph] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [error, setError] = useState("");
  const [elements , setElements] = useState([]);
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isZoomed, setIsZoomed] = useState(false);
  const [url, setUrl] = useState("");
  const [gbtJson,setGbtJson]= useState("");

  var elms = [] ;


  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setImageSrc("");
    setLoading(true); 
  
    let data = {
      "desc": paragraph,
      "elements": elements
    };
    try{
      console.log("Sending data:", data);
    
      const response = await fetch("http://localhost:8080/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({data})
      });
    
      const resJson = await response.json();
      console.log("Received from server:", resJson);

      if (resJson!= null) {
        // 2. Send GET to fetch the generated image
        const imageUrl = 'http://localhost:8080/text';
        setImageSrc(imageUrl);
        console.log("image done")
      } else {
        console.error('Image generation failed:', resJson.error);
      } 

      
      const gbtResponse = await fetch("http://127.0.0.1:5000/run_gbt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          input: paragraph,
          layers: elements,
          layout: "dot"
        })
      });
      
      const data1 = await gbtResponse.json();  // data1 = { result: "some-url" }
      setGbtJson(data1.result);  // set the URL only
      
      if (data1.result) {
        console.log("Received from Python run_gbt:", data1.result);
      } else {
        console.log("url empty");
      }




    }catch (err) {
      console.error("Error during fetch:", err);
    } finally {
      setLoading(false); // hide the loading message
    }
  };
  const handlechek = async (e) =>{
    const elm = e.target.name
    const isChecked = e.target.checked;
    setElements((prev) => {
        if (isChecked) {
          return [...prev,elm]; // add if checked
        } else {
          return prev.filter((item) => item !== elm); // remove if unchecked
        }
      });
    
  }

  return (
    <div className="container">
      <h1>Archimate Diagram Generator</h1>
      <h4>Enter your project description, chose layers and press generate</h4>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={6}
          placeholder="Enter a paragraph"
          value={paragraph}
          onChange={(e) => setParagraph(e.target.value)}
        />
        <div className="check_container">
            <span className="chek">
                <input type="checkbox" id="Business" name="Business" onChange={handlechek}/>
                <label htmlFor="">Business</label>
            </span>
            <span className="chek">
                <input type="checkbox" id="Application" name="Application" onChange={handlechek}/>
                <label htmlFor="">Application</label>
            </span>
            <span className="chek">
                <input type="checkbox" id="Motivation" name="Motivation" onChange={handlechek}/>
                <label htmlFor="">Motivation</label>
            </span>
            <span className="chek">
                <input type="checkbox" id="Technologie" name="Technologie" onChange={handlechek}/>
                <label htmlFor="">Technologie</label>
            </span>
            <span className="chek">
                <input type="checkbox" id="Strategy" name="Strategy" onChange={handlechek}/>
                <label htmlFor="">Strategy</label>
            </span>
        </div>
        <button type="submit">Generate Image</button>
      </form>
      {loading && <p>This may take a while, please wait...</p>}
      
      {imageSrc && (
        <div className="image-container">
          <Zoom>
            <img
              src={imageSrc}
              alt="Generated"
              style={{
                display: imageSrc ? "block" : "none",
                height: "auto",
                objectFit: "contain"
              }}
              onError={(e) => {
                e.target.style.display = "none";
                console.error("Failed to load image:", imageSrc);
              }}
            />
          </Zoom>
          {gbtJson &&
            <a 
              href= {gbtJson}           
              className="download-button"
              target="_blank"
            >
              View Drow.io version
            </a>
          }
        </div>
      )}
          
      {/* {error && <p className="error">{error}</p>}
      {imageUrl && <img src={imageUrl} alt="Generated" className="result-image" />} */}
    </div>
  );
}

export default Content;
