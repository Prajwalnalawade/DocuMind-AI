import { useState } from "react";

import {
  uploadDocument,
  analyzeDocument,
} from "../services/documentService";


function UploadDocument() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState("");


  // =========================================================
  // FILE SELECTION
  // =========================================================

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    setError("");
    setUploadResult(null);
    setAnalysisResult(null);

    if (!file) {
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };


  // =========================================================
  // UPLOAD
  // =========================================================

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a document first.");
      return;
    }

    setIsUploading(true);
    setError("");
    setUploadResult(null);
    setAnalysisResult(null);

    try {
      const result = await uploadDocument(selectedFile);

      setUploadResult(result);
      setSelectedFile(null);

    } catch (err) {
      console.error("Upload failed:", err);

      const detail = err.response?.data?.detail;

      let message = "Unable to upload the document.";

      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        message = detail
          .map((item) => item.msg || "Validation error")
          .join(", ");
      }

      setError(message);

    } finally {
      setIsUploading(false);
    }
  };


  // =========================================================
  // ANALYZE
  // =========================================================

  const handleAnalyze = async () => {
    if (!uploadResult?.document_id) {
      setError("Please upload a document before analyzing it.");
      return;
    }

    setIsAnalyzing(true);
    setError("");
    setAnalysisResult(null);

    try {
      const result = await analyzeDocument(
        uploadResult.document_id
      );

      setAnalysisResult(result);

    } catch (err) {
      console.error("Analysis failed:", err);

      const detail = err.response?.data?.detail;

      let message = "Unable to analyze the document.";

      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        message = detail
          .map((item) => item.msg || "Validation error")
          .join(", ");
      }

      setError(message);

    } finally {
      setIsAnalyzing(false);
    }
  };


  // =========================================================
  // DATA
  // =========================================================

  const structuredData = analysisResult?.structured_data;
  const validation = analysisResult?.validation;
  const summary = analysisResult?.summary;


  const validationStatus = validation?.status;

  const validationLabel =
    validationStatus === "valid"
      ? "VALID"
      : validationStatus === "valid_with_warnings"
        ? "VALID WITH WARNINGS"
        : validationStatus === "invalid"
          ? "INVALID"
          : "UNKNOWN";


  const validationIcon =
    validationStatus === "valid"
      ? "✓"
      : validationStatus === "valid_with_warnings"
        ? "⚠"
        : validationStatus === "invalid"
          ? "✕"
          : "?";


  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="upload-page">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="analysis-header">

        <div>
          <h1>DocuMind AI</h1>

          <p>
            Intelligent Document Analysis
          </p>
        </div>

      </div>


      {/* =====================================================
          UPLOAD SECTION
      ===================================================== */}

      <div className="upload-card">

        <h2>
          Upload Document
        </h2>

        <p>
          Upload an invoice, quotation, contract,
          receipt, or other business document.
        </p>


        <label className="file-input-label">

          Select Document

          <input
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileChange}
          />

        </label>


        {selectedFile && (
          <div className="selected-file">

            <h3>
              Selected File
            </h3>

            <p>
              <strong>Name:</strong>{" "}
              {selectedFile.name}
            </p>

            <p>
              <strong>Size:</strong>{" "}
              {(selectedFile.size / 1024).toFixed(2)} KB
            </p>

            <p>
              <strong>Type:</strong>{" "}
              {selectedFile.type || "Unknown"}
            </p>

          </div>
        )}


        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={
            !selectedFile ||
            isUploading ||
            isAnalyzing
          }
        >

          {isUploading
            ? "Uploading..."
            : "Upload Document"}

        </button>


        {/* ===================================================
            ERROR
        =================================================== */}

        {error && (
          <div className="upload-error">

            <strong>
              Error
            </strong>

            <p>
              {error}
            </p>

          </div>
        )}


        {/* ===================================================
            UPLOAD SUCCESS
        =================================================== */}

        {uploadResult && (
          <div className="upload-success">

            <h3>
              ✓ Document Uploaded
            </h3>

            <p>
              <strong>Filename:</strong>{" "}
              {uploadResult.filename}
            </p>

            <p>
              <strong>Document ID:</strong>{" "}
              {uploadResult.document_id}
            </p>


            <button
              className="upload-button"
              onClick={handleAnalyze}
              disabled={isAnalyzing}
            >

              {isAnalyzing
                ? "Analyzing..."
                : "Analyze Document"}

            </button>

          </div>
        )}

      </div>


      {/* =====================================================
          ANALYSIS LOADING
      ===================================================== */}

      {isAnalyzing && (
        <div className="analysis-loading">

          <div className="loading-icon">
            🤖
          </div>

          <h2>
            Analyzing Document
          </h2>

          <p>
            DocuMind AI is extracting information,
            validating the document, and generating
            an intelligent summary.
          </p>

          <div className="loading-steps">

            <span>
              ✓ Text Extraction
            </span>

            <span>
              ✓ AI Extraction
            </span>

            <span>
              ✓ Validation
            </span>

            <span>
              • AI Summary
            </span>

          </div>

        </div>
      )}


      {/* =====================================================
          ANALYSIS DASHBOARD
      ===================================================== */}

      {analysisResult && (
        <div className="analysis-dashboard">

          {/* =================================================
              TOP CARDS
          ================================================= */}

          <div className="analysis-card-grid">

            <div className="analysis-stat-card">

              <div className="stat-icon">
                📄
              </div>

              <div>

                <span className="stat-label">
                  Document Type
                </span>

                <strong className="stat-value">
                  {structuredData?.document_type ||
                    "Unknown"}
                </strong>

              </div>

            </div>


            <div className="analysis-stat-card">

              <div className="stat-icon">
                🔍
              </div>

              <div>

                <span className="stat-label">
                  Validation
                </span>

                <strong className="stat-value">
                  {validationIcon}{" "}
                  {validationLabel}
                </strong>

              </div>

            </div>


            <div className="analysis-stat-card">

              <div className="stat-icon">
                ⭐
              </div>

              <div>

                <span className="stat-label">
                  Validation Score
                </span>

                <strong className="stat-value">
                  {validation?.score ?? 0}%
                </strong>

              </div>

            </div>

          </div>


          {/* =================================================
              AI OVERVIEW
          ================================================= */}

          <section className="analysis-section">

            <div className="section-heading">

              <span>
                🤖
              </span>

              <h2>
                AI Overview
              </h2>

            </div>

            <p className="overview-text">
              {summary?.overview ||
                "No summary available."}
            </p>

          </section>


          {/* =================================================
              DOCUMENT + VENDOR
          ================================================= */}

          <div className="analysis-two-column">

            <section className="analysis-section">

              <div className="section-heading">

                <span>
                  📋
                </span>

                <h2>
                  Document Information
                </h2>

              </div>


              <div className="detail-list">

                <div className="detail-row">

                  <span>
                    Document Type
                  </span>

                  <strong>
                    {structuredData?.document_type ||
                      "Not available"}
                  </strong>

                </div>


                <div className="detail-row">

                  <span>
                    Title
                  </span>

                  <strong>
                    {structuredData?.document_title ||
                      "Not available"}
                  </strong>

                </div>


                <div className="detail-row">

                  <span>
                    Document Number
                  </span>

                  <strong>
                    {structuredData?.document_number ||
                      "Not available"}
                  </strong>

                </div>


                <div className="detail-row">

                  <span>
                    Document Date
                  </span>

                  <strong>
                    {structuredData?.document_date ||
                      "Not available"}
                  </strong>

                </div>


                <div className="detail-row">

                  <span>
                    Valid Until
                  </span>

                  <strong>
                    {structuredData?.valid_until ||
                      "Not available"}
                  </strong>

                </div>

              </div>

            </section>


            <section className="analysis-section">

              <div className="section-heading">

                <span>
                  🏢
                </span>

                <h2>
                  Vendor
                </h2>

              </div>


              <div className="detail-list">

                <div className="detail-row">

                  <span>
                    Name
                  </span>

                  <strong>
                    {structuredData?.vendor?.name ||
                      "Not available"}
                  </strong>

                </div>


                <div className="detail-row">

                  <span>
                    Phone
                  </span>

                  <strong>
                    {structuredData?.vendor?.phone ||
                      "Not available"}
                  </strong>

                </div>


                <div className="detail-row">

                  <span>
                    Email
                  </span>

                  <strong>
                    {structuredData?.vendor?.email ||
                      "Not available"}
                  </strong>

                </div>

              </div>

            </section>

          </div>


          {/* =================================================
              KEY POINTS
          ================================================= */}

          {summary?.key_points?.length > 0 && (

            <section className="analysis-section">

              <div className="section-heading">

                <span>
                  ✨
                </span>

                <h2>
                  Key Points
                </h2>

              </div>


              <div className="bullet-grid">

                {summary.key_points.map(
                  (point, index) => (

                    <div
                      className="bullet-item"
                      key={index}
                    >

                      <span>
                        ✓
                      </span>

                      <p>
                        {point}
                      </p>

                    </div>

                  )
                )}

              </div>

            </section>

          )}


          {/* =================================================
              ITEMS / SERVICES
          ================================================= */}

          {summary?.items_summary && (

            <section className="analysis-section">

              <div className="section-heading">

                <span>
                  📦
                </span>

                <h2>
                  Items & Services
                </h2>

              </div>

              <p>
                {summary.items_summary}
              </p>

            </section>

          )}


          {/* =================================================
              FINANCIAL SUMMARY
          ================================================= */}

          {summary?.financial_summary && (

            <section className="analysis-section">

              <div className="section-heading">

                <span>
                  💰
                </span>

                <h2>
                  Financial Summary
                </h2>

              </div>


              <div className="financial-grid">

                <div>
                  <span>
                    Currency
                  </span>

                  <strong>
                    {summary.financial_summary.currency ||
                      "Not available"}
                  </strong>
                </div>


                <div>
                  <span>
                    Subtotal
                  </span>

                  <strong>
                    {summary.financial_summary.subtotal ??
                      "Not available"}
                  </strong>
                </div>


                <div>
                  <span>
                    Discount
                  </span>

                  <strong>
                    {summary.financial_summary.discount ??
                      "Not available"}
                  </strong>
                </div>


                <div>
                  <span>
                    Tax
                  </span>

                  <strong>
                    {summary.financial_summary.tax ??
                      "Not available"}
                  </strong>
                </div>


                <div>
                  <span>
                    Shipping
                  </span>

                  <strong>
                    {summary.financial_summary.shipping ??
                      "Not available"}
                  </strong>
                </div>


                <div className="financial-total">

                  <span>
                    Total
                  </span>

                  <strong>
                    {summary.financial_summary.total ??
                      "Not available"}
                  </strong>

                </div>

              </div>


              {summary.financial_summary.explanation && (

                <p className="financial-explanation">
                  {summary.financial_summary.explanation}
                </p>

              )}

            </section>

          )}


          {/* =================================================
              PAYMENT + DELIVERY
          ================================================= */}

          <div className="analysis-two-column">

            {summary?.payment_terms && (

              <section className="analysis-section">

                <div className="section-heading">

                  <span>
                    💳
                  </span>

                  <h2>
                    Payment Terms
                  </h2>

                </div>

                <p>
                  {summary.payment_terms}
                </p>

              </section>

            )}


            {summary?.delivery_terms && (

              <section className="analysis-section">

                <div className="section-heading">

                  <span>
                    🚚
                  </span>

                  <h2>
                    Delivery Terms
                  </h2>

                </div>

                <p>
                  {summary.delivery_terms}
                </p>

              </section>

            )}

          </div>


          {/* =================================================
              IMPORTANT TERMS
          ================================================= */}

          {summary?.important_terms?.length > 0 && (

            <section className="analysis-section">

              <div className="section-heading">

                <span>
                  📑
                </span>

                <h2>
                  Important Terms
                </h2>

              </div>


              <div className="bullet-grid">

                {summary.important_terms.map(
                  (term, index) => (

                    <div
                      className="bullet-item"
                      key={index}
                    >

                      <span>
                        •
                      </span>

                      <p>
                        {term}
                      </p>

                    </div>

                  )
                )}

              </div>

            </section>

          )}


          {/* =================================================
              VALIDATION
          ================================================= */}

          {validation && (

            <section className="analysis-section">

              <div className="section-heading">

                <span>
                  🔍
                </span>

                <h2>
                  Validation Result
                </h2>

              </div>


              <div className="validation-overview">

                <div className="validation-main">

                  <span className="validation-icon">
                    {validationIcon}
                  </span>

                  <div>

                    <strong>
                      {validationLabel}
                    </strong>

                    <p>
                      {validation.summary}
                    </p>

                  </div>

                </div>


                <div className="validation-score">

                  <span>
                    Score
                  </span>

                  <strong>
                    {validation.score}%
                  </strong>

                </div>

              </div>


              <div className="validation-stats">

                <div>
                  <strong>
                    {validation.total_checks}
                  </strong>

                  <span>
                    Total Checks
                  </span>
                </div>


                <div>
                  <strong>
                    {validation.passed_checks}
                  </strong>

                  <span>
                    Passed
                  </span>
                </div>


                <div>
                  <strong>
                    {validation.error_count ?? 0}
                  </strong>

                  <span>
                    Errors
                  </span>
                </div>


                <div>
                  <strong>
                    {validation.warning_count}
                  </strong>

                  <span>
                    Warnings
                  </span>
                </div>

              </div>

            </section>

          )}


          {/* =================================================
              VALIDATION FINDINGS
          ================================================= */}

          {validation?.issues?.length > 0 && (

            <section className="analysis-section warning-section">

              <div className="section-heading">

                <span>
                  ⚠️
                </span>

                <h2>
                  Validation Findings
                </h2>

              </div>


              <div className="warning-list">

                {validation.issues.map(
                  (issue, index) => (

                    <div
                      className="warning-item"
                      key={index}
                    >

                      <strong>
                        {issue.severity?.toUpperCase()}
                      </strong>

                      <p>
                        {issue.message}
                      </p>

                    </div>

                  )
                )}

              </div>

            </section>

          )}


          {/* =================================================
              AI WARNINGS
          ================================================= */}

          {summary?.warnings?.length > 0 && (

            <section className="analysis-section warning-section">

              <div className="section-heading">

                <span>
                  ⚠️
                </span>

                <h2>
                  AI Warnings
                </h2>

              </div>


              <div className="bullet-grid">

                {summary.warnings.map(
                  (warning, index) => (

                    <div
                      className="bullet-item"
                      key={index}
                    >

                      <span>
                        !
                      </span>

                      <p>
                        {warning}
                      </p>

                    </div>

                  )
                )}

              </div>

            </section>

          )}


          {/* =================================================
              RECOMMENDATION
          ================================================= */}

          {summary?.recommendation && (

            <section className="analysis-section recommendation-section">

              <div className="section-heading">

                <span>
                  💡
                </span>

                <h2>
                  AI Recommendation
                </h2>

              </div>

              <p>
                {summary.recommendation}
              </p>

            </section>

          )}


          {/* =================================================
              SOURCE INFORMATION
          ================================================= */}

          {analysisResult?.source_text && (

            <div className="source-information">

              <span>
                Source:{" "}
                {analysisResult.source_text.extraction_method}
              </span>

              <span>
                Pages:{" "}
                {analysisResult.source_text.page_count}
              </span>

              <span>
                Characters:{" "}
                {analysisResult.source_text.character_count}
              </span>

            </div>

          )}

        </div>
      )}

    </div>
  );
}


export default UploadDocument;