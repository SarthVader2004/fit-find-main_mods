import React from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const { pathname } = useLocation();

  return (
    <nav className="navbar">
      <div className="nav-logo">👗 FitFind</div>
      <div className="nav-links">
        <Link to="/" className={pathname === "/" ? "active" : ""}>Home</Link>
        <Link to="/chatbot" className={pathname === "/chatbot" ? "active" : ""}>Chatbot</Link>
        <Link to="/bodytype" className={pathname === "/bodytype" ? "active" : ""}>Body Type</Link>
        <Link to="/tryon" className={pathname === "/tryon" ? "active" : ""}>Virtual Try-On</Link>
        
      </div>
    </nav>
  );
};

export default Navbar;
