import {useNavigate} from 'react-router-dom';
import './App.css';

function Landing(){
  const navigate=useNavigate();
  const handleGetStarted=()=>{
    navigate('/dashboard');
  };
  return (
    <>
    <div className="image">
    <div className="overlay"></div>
    <div className="content">
      Welcome To<br/>SenTech
    </div>
    <div className="centerAlign">
    <button className="getStartedButton" onClick={handleGetStarted}>Get Started</button>
    </div>
    </div>
    </>
  );
}

function LandingPage() {
  return (
    <>
    <Landing />
    </>
  );
}

export default LandingPage;
