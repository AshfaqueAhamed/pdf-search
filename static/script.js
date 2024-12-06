// Using pdf.js library with worker setup

// Ensure the path to the worker script is correct
pdfjsLib.GlobalWorkerOptions.workerSrc = '/static/pdf.worker.js';  // Correct path to the worker script

// DOM elements
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const searchResults = document.getElementById('search-results');
const canvasContainer = document.getElementById('canvas-container'); // Add a container for multiple pages

// Event listener for the Search button
searchBtn.addEventListener('click', async () => {
  const keyword = searchInput.value.trim();
  
  if (!keyword) {
    alert('Please enter a keyword to search.');
    return;
  }

  try {
    // Fetch search results from the API
    const response = await fetch(`/search?keyword=${encodeURIComponent(keyword)}`);
    if (!response.ok) throw new Error('Error fetching search results');

    const data = await response.json();

    if (data.results.length === 0) {
      searchResults.innerHTML = '<p>No results found.</p>';
      return;
    }

    // Display the search results
    searchResults.innerHTML = data.results
      .map(result => `
        <div class="result-item">
          <p><strong>${result.filename}</strong></p>
          <p>${result.snippet}</p>
          <button onclick="openPdf('${result.filename}', '${keyword}')">Open PDF</button>
        </div>
      `)
      .join('');
  } catch (error) {
    console.error('Search Error:', error);
    searchResults.innerHTML = '<p>An error occurred while searching. Please try again.</p>';
  }
});

// Function to open a PDF and render it in the custom viewer
async function openPdf(filename, keyword) {
  const url = `/pdfs/${filename}`; // Adjusted to match your folder structure
  const loadingTask = pdfjsLib.getDocument(url);

  try {
    const pdf = await loadingTask.promise;
    const numPages = pdf.numPages;
    canvasContainer.innerHTML = ''; // Clear previous renders

    // Loop through pages and render each one
    for (let pageNum = 1; pageNum <= numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const viewport = page.getViewport({ scale: 1.5 });

      // Create a canvas for each page
      const canvas = document.createElement('canvas');
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      canvasContainer.appendChild(canvas);

      const renderContext = {
        canvasContext: canvas.getContext('2d'),
        viewport: viewport,
      };

      await page.render(renderContext).promise;

      // Highlight the text after rendering
      highlightText(page, keyword, viewport, canvas);
    }
  } catch (error) {
    console.error('PDF Loading Error:', error);
    alert('Error loading the PDF. Please check the file.');
  }
}

// Function to highlight the search keyword in the PDF
async function highlightText(page, keyword, viewport, context) {
  const textContent = await page.getTextContent();

  context.globalAlpha = 0.4; // Make the highlight semi-transparent
  context.fillStyle = 'yellow';

  textContent.items.forEach(item => {
    if (item.str.toLowerCase().includes(keyword.toLowerCase())) {
      const [x, y] = item.transform.slice(4);
      const width = item.width * viewport.transform[0];
      const height = 10; // Approximate height of the text

      // Draw highlight rectangle
      context.fillRect(x, viewport.height - y, width, height);
    }
  });
}
