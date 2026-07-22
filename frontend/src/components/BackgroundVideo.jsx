import React from "react";
import "../App.css"; // for the .bg-video class

const BackgroundVideo = React.memo(() => {
  return (
    <video className="bg-video" autoPlay loop muted playsInline>
      <source src="/videos/bg1.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  );
});

export default BackgroundVideo;
