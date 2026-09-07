import api from "./api";

// =========================================================
// BACKEND HEALTH
// =========================================================

export const checkBackendHealth = async () => {
  const response = await api.get("/health");

  return response.data;
};


// =========================================================
// UPLOAD DOCUMENT
// =========================================================

export const uploadDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/documents/upload",
    formData
  );

  return response.data;
};


// =========================================================
// EXTRACT STRUCTURED DOCUMENT DATA
// =========================================================

export const extractDocument = async (documentId) => {
  const response = await api.post(
    `/documents/${documentId}/extract`
  );

  return response.data;
};


// =========================================================
// VALIDATE DOCUMENT
// =========================================================

export const validateDocument = async (documentId) => {
  const response = await api.post(
    `/documents/${documentId}/validate`
  );

  return response.data;
};


// =========================================================
// GENERATE AI DOCUMENT SUMMARY
// =========================================================

export const summarizeDocument = async (documentId) => {
  const response = await api.post(
    `/documents/${documentId}/summary`
  );

  return response.data;
};


// =========================================================
// COMPLETE DOCUMENT ANALYSIS
// =========================================================

export const analyzeDocument = async (documentId) => {
  const response = await api.post(
    `/documents/${documentId}/summary`
  );

  return response.data;
};