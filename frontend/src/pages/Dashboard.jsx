import { useEffect, useState } from "react";

import { checkBackendHealth } from "../services/documentService";


function Dashboard() {
  const [backendStatus, setBackendStatus] =
    useState("Checking...");

  const [error, setError] = useState("");


  // =========================================================
  // BACKEND HEALTH CHECK
  // =========================================================

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const data = await checkBackendHealth();

        if (data.status === "healthy") {
          setBackendStatus("Connected");
        } else {
          setBackendStatus("Unavailable");
        }

      } catch (err) {
        console.error(
          "Backend connection failed:",
          err
        );

        setBackendStatus("Disconnected");

        setError(
          "Unable to connect to the backend."
        );
      }
    };

    checkConnection();
  }, []);


  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="dashboard-page">

      {/* =====================================================
          HERO
      ===================================================== */}

      <section className="dashboard-hero">

        <div className="dashboard-hero-content">

          <div className="dashboard-badge">
            <span className="dashboard-badge-dot"></span>

            AI-Powered Document Intelligence
          </div>


          <h1>
            Understand Your Documents
            <span> Smarter with AI</span>
          </h1>


          <p>
            DocuMind AI extracts information, validates
            business documents, and generates intelligent
            summaries in seconds.
          </p>


          <div className="dashboard-actions">

            <a
              href="/upload"
              className="dashboard-primary-button"
            >
              <span>📄</span>
              Upload Document
            </a>


            <a
              href="/upload"
              className="dashboard-secondary-button"
            >
              Analyze Document
              <span>→</span>
            </a>

          </div>

        </div>


        {/* =================================================
            HERO VISUAL
        ================================================= */}

        <div className="dashboard-hero-visual">

          <div className="document-preview-card">

            <div className="document-preview-top">

              <div className="document-preview-icon">
                📄
              </div>

              <div>

                <strong>
                  Business Document
                </strong>

                <span>
                  AI Analysis Ready
                </span>

              </div>

            </div>


            <div className="document-preview-lines">

              <div className="preview-line large"></div>

              <div className="preview-line"></div>

              <div className="preview-line medium"></div>

              <div className="preview-line"></div>

              <div className="preview-line small"></div>

            </div>


            <div className="document-preview-result">

              <span>
                ✓
              </span>

              <div>

                <strong>
                  Document Validated
                </strong>

                <small>
                  AI extraction completed
                </small>

              </div>

            </div>

          </div>

        </div>

      </section>


      {/* =====================================================
          PLATFORM FEATURES
      ===================================================== */}

      <section className="dashboard-features">

        <div className="dashboard-section-heading">

          <span>
            Powerful document intelligence
          </span>

          <h2>
            Everything you need to understand documents
          </h2>

          <p>
            From raw documents to actionable business
            insights, DocuMind AI handles the complete
            analysis pipeline.
          </p>

        </div>


        <div className="feature-grid">

          {/* =================================================
              FEATURE 1
          ================================================= */}

          <div className="feature-card">

            <div className="feature-icon">
              📑
            </div>

            <h3>
              Smart Extraction
            </h3>

            <p>
              Extract document information such as
              vendors, customers, dates, line items,
              totals, and business terms.
            </p>

          </div>


          {/* =================================================
              FEATURE 2
          ================================================= */}

          <div className="feature-card">

            <div className="feature-icon">
              🔍
            </div>

            <h3>
              Document Validation
            </h3>

            <p>
              Automatically check financial calculations,
              dates, quantities, totals, and other
              business rules.
            </p>

          </div>


          {/* =================================================
              FEATURE 3
          ================================================= */}

          <div className="feature-card">

            <div className="feature-icon">
              🤖
            </div>

            <h3>
              AI Summaries
            </h3>

            <p>
              Convert complex business documents into
              concise and understandable summaries with
              important points and recommendations.
            </p>

          </div>

        </div>

      </section>


      {/* =====================================================
          PROCESSING PIPELINE
      ===================================================== */}

      <section className="dashboard-pipeline">

        <div className="dashboard-section-heading">

          <span>
            How it works
          </span>

          <h2>
            From document to insight
          </h2>

        </div>


        <div className="pipeline-container">

          {/* =================================================
              STEP 1
          ================================================= */}

          <div className="pipeline-step">

            <div className="pipeline-number">
              01
            </div>

            <div className="pipeline-icon">
              📤
            </div>

            <h3>
              Upload
            </h3>

            <p>
              Upload your invoice, quotation,
              receipt, or contract.
            </p>

          </div>


          <div className="pipeline-connector">
            →
          </div>


          {/* =================================================
              STEP 2
          ================================================= */}

          <div className="pipeline-step">

            <div className="pipeline-number">
              02
            </div>

            <div className="pipeline-icon">
              🧠
            </div>

            <h3>
              Extract
            </h3>

            <p>
              AI extracts meaningful structured
              information from the document.
            </p>

          </div>


          <div className="pipeline-connector">
            →
          </div>


          {/* =================================================
              STEP 3
          ================================================= */}

          <div className="pipeline-step">

            <div className="pipeline-number">
              03
            </div>

            <div className="pipeline-icon">
              🔎
            </div>

            <h3>
              Validate
            </h3>

            <p>
              Business rules identify errors,
              inconsistencies, and warnings.
            </p>

          </div>


          <div className="pipeline-connector">
            →
          </div>


          {/* =================================================
              STEP 4
          ================================================= */}

          <div className="pipeline-step">

            <div className="pipeline-number">
              04
            </div>

            <div className="pipeline-icon">
              💡
            </div>

            <h3>
              Understand
            </h3>

            <p>
              Receive an AI-generated summary,
              warnings, and recommendations.
            </p>

          </div>

        </div>

      </section>


      {/* =====================================================
          SYSTEM STATUS
      ===================================================== */}

      <section className="dashboard-system">

        <div className="system-status-card">

          <div className="system-status-icon">
            {backendStatus === "Connected"
              ? "✓"
              : "!"}
          </div>


          <div className="system-status-content">

            <span>
              System Status
            </span>

            <strong>
              Backend {backendStatus}
            </strong>

            {error && (
              <p>
                {error}
              </p>
            )}

          </div>


          <div
            className={`system-status-indicator ${
              backendStatus === "Connected"
                ? "online"
                : "offline"
            }`}
          >
            <span></span>

            {backendStatus}
          </div>

        </div>

      </section>


      {/* =====================================================
          FINAL CTA
      ===================================================== */}

      <section className="dashboard-cta">

        <div>

          <span>
            Ready to analyze your documents?
          </span>

          <h2>
            Turn documents into useful insights.
          </h2>

          <p>
            Upload your first document and let
            DocuMind AI do the analysis.
          </p>

        </div>


        <a
          href="/upload"
          className="dashboard-cta-button"
        >
          Get Started
          <span>→</span>
        </a>

      </section>

    </div>
  );
}


export default Dashboard;