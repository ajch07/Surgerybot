import { useRef, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import './index.css';

// import "react-pdf/dist/esm/Page/AnnotationLayer.css";
// import "react-pdf/dist/esm/Page/TextLayer.css";

const PDF_URL = "/manual_compressed.pdf"; // Make sure manual.pdf is in your public folder

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function App() {
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [numPages, setNumPages] = useState(null);
  const [pdfPage, setPdfPage] = useState(1);
  const pdfWrapperRef = useRef();

  const sendQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setChat([...chat, { sender: "you", text: query }]);
    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setChat((prev) => [
        ...prev,
        { sender: "tutor", text: data.answer, pages: data.pages }
      ]);
    } catch (e) {
      setChat((prev) => [
        ...prev,
        { sender: "tutor", text: "Error contacting the tutor.", pages: [] }
      ]);
    }
    setQuery("");
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendQuery();
    }
  };

  // When a page button is clicked, set the PDF viewer to that page
  const goToPage = (page) => {
    setPdfPage(page);
    pdfWrapperRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div style={{
      display: "flex",
      height: "100vh",
      width: "100vw",
      background: "#f4f4f4"
    }}>
      {/* Left Pane: PDF Viewer */}
      <div
        ref={pdfWrapperRef}
        style={{
          flex: 1,
          background: "#222",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          height: "100vh",
          minWidth: 0,
          boxShadow: "2px 0 8px rgba(0,0,0,0.08)",
          padding: 0,
        }}
      >
        <div style={{
          width: "100%",
          maxWidth: 520,
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: 24,
          background: "#23272f",
          borderRadius: 0,
          margin: 0,
          boxShadow: "0 2px 12px rgba(0,0,0,0.10)",
          overflow: "hidden"
        }}>
          <div style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "100%",
            overflow: "hidden"
          }}>
            <Document
              file={PDF_URL}
              onLoadSuccess={({ numPages }) => setNumPages(numPages)}
              loading="Loading PDF..."
            >
              <Page pageNumber={pdfPage} width={470} />
            </Document>
          </div>
          <div style={{
            textAlign: "center",
            marginTop: 18,
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
          }}>
            <button
              onClick={() => setPdfPage((p) => Math.max(1, p - 1))}
              disabled={pdfPage <= 1}
              style={{
                marginRight: 18,
                padding: "6px 18px",
                borderRadius: 6,
                border: "none",
                background: "#007bff",
                color: "#fff",
                fontWeight: 500,
                cursor: pdfPage <= 1 ? "not-allowed" : "pointer",
                opacity: pdfPage <= 1 ? 0.5 : 1
              }}
            >Prev</button>
            <span style={{ color: "#fff", fontWeight: 500, fontSize: 16 }}>
              Page {pdfPage} of {numPages || "..."}
            </span>
            <button
              onClick={() => setPdfPage((p) => Math.min(numPages, p + 1))}
              disabled={pdfPage >= numPages}
              style={{
                marginLeft: 18,
                padding: "6px 18px",
                borderRadius: 6,
                border: "none",
                background: "#007bff",
                color: "#fff",
                fontWeight: 500,
                cursor: pdfPage >= numPages ? "not-allowed" : "pointer",
                opacity: pdfPage >= numPages ? 0.5 : 1
              }}
            >Next</button>
          </div>
        </div>
      </div>

      {/* Right Pane: Chatbot */}
      <div style={{
        flex: 1,
        background: "#fff",
        display: "flex",
        flexDirection: "column",
        height:"100vh",
        justifyContent: "flex-end",
        borderLeft: "1px solid #ddd",
        minWidth: 0
      }}>
        <div style={{
          flex: 1,
          overflowY: "auto",
          padding: 24,
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-end"
        }}>
          <h2 style={{ textAlign: "center" }}>Surgery Tutor Chatbot</h2>
          <div style={{
            minHeight: 120,
            maxHeight: 350,
            marginBottom: 20,
            background: "#f9f9f9",
            padding: 15,
            borderRadius: 10,
            border: "1px solid #d0d7de",
            overflowY: "auto",
            wordBreak: "break-word",
            fontFamily: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif",
            fontSize: 16,
            boxShadow: "0 2px 12px rgba(0,0,0,0.06)"
            }}>
        {chat.map((msg, idx) => (
                <div
                    key={idx}
                    style={{
                    margin: "14px 0",
                    padding: "12px 16px",
                    borderRadius: 8,
                    background: msg.sender === "you" ? "#e3f0ff" : "#fff",
                    color: "#222",
                    alignSelf: msg.sender === "you" ? "flex-end" : "flex-start",
                    boxShadow: msg.sender === "you"
                    ? "0 1px 4px rgba(0,123,255,0.08)"
                    : "0 1px 4px rgba(0,0,0,0.04)",
                    maxWidth: "85%",
                    border: msg.sender === "you"
                    ? "1px solid #b6d4fe"
                    : "1px solid #e0e0e0"
                }}
                >
            <b style={{
                color: msg.sender === "you" ? "#007bff" : "#222",
                fontWeight: 600
            }}>
                {msg.sender === "you" ? "You" : "Tutor"}:
                </b>{" "}
                <span dangerouslySetInnerHTML={{ __html: msg.text }} />
                {/* Page number buttons */}
                {msg.sender === "tutor" && msg.pages && msg.pages.length > 0 && (
                <div style={{ marginTop: 8 }}>
                {msg.pages.map((page, i) => (
                    <button
                        key={i}
                        onClick={() => goToPage(page)}
                    style={{
                            marginRight: 6,
                            padding: "2px 10px",
                            borderRadius: 4,
                            border: "1px solid #007bff",
                            background: "#eaf2ff",
                            color: "#007bff",
                            cursor: "pointer",
                            fontSize: 14
                            }}
                        >
                        Page {page}
                        </button>
                    ))}
                    </div>
                )}
                </div>
            ))}
            {loading && <div><b>Tutor:</b> Thinking...</div>}
            </div>
            </div>
            <div style={{ padding: 18, borderTop: "1px solid #eee" }}>
            <textarea
            rows={2}
            style={{ width: "100%", padding: 8, borderRadius: 4, border: "1px solid #ccc" }}
            placeholder="Ask your surgery question..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <button
            style={{
              padding: "8px 16px", border: "none", background: "#007bff",
              color: "#fff", borderRadius: 4, cursor: "pointer", marginTop: 8, float: "right"
            }}
            onClick={sendQuery}
            disabled={loading}
          >
            Send
          </button>
          <div style={{ clear: "both" }}></div>
        </div>
      </div>
    </div>
  );
}

export default App;