// src/Layout.js
import React from 'react';
import { Outlet } from 'react-router-dom';
import './dashboard_style.css'; // Import your CSS here

const Layout = () => {
  return (
    <div className="container">
      <div className="sidebar">
        <h2>Maintenance</h2>
        <nav>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="#">Status History</a></li>
            <li><a href="#">About</a></li>
          </ul>
        </nav>
      </div>

      <div className="main-content">
        <Outlet />
      </div>
    </div>
  );
}

export default Layout;
