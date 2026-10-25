type ErrorEnvelope = {
  error?: { message?: string; details?: { field: string; reason: string }[] };
};

export function apiError(payload: unknown, status: number): string {
  const error = (payload as ErrorEnvelope | null)?.error;
  const fallback: Record<number, string> = {
    401: "Sign-in failed or your session expired. Check your credentials and sign in again.",
    403: "You do not have permission for this action in the selected organization.",
    404: "The requested record is not available.",
    409: "This operation conflicts with the current state. Reload and try again.",
    413: "This import exceeds the size limit. Split it into smaller batches.",
    422: "Check the highlighted fields and try again.",
    429: "Too many attempts. Wait before trying again.",
  };
  const message =
    error?.message ||
    fallback[status] ||
    "The service is unavailable. Try again.";
  const fields = error?.details?.map(
    (d) => `${d.field.replace(/^body\./, "")}: ${d.reason}`,
  );
  return fields?.length ? `${message} ${fields.join("; ")}` : message;
}
