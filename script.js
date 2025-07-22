document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
  
    document.getElementById("status").textContent = "Processing...";
  
    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData
      });
  
      if (!response.ok) {
        throw new Error("Failed to generate report.");
      }
  
      const blob = await response.blob();
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = "report.pdf";
      link.click();
  
      document.getElementById("status").textContent = "Report downloaded!";
    } catch (error) {
      document.getElementById("status").textContent = error.message;
    }
  });
  