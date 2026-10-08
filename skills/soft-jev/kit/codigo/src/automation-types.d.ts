import type { Result, Arguments } from './types.js';

export type Phase = 'prepare' | 'delegate' | 'memory' | 'collect' | 'observe' | 'file_review';
export interface Candidate { id: string; description?: string }
export interface AutomationEvent {
  event: Phase;
  harness: string;
  session_id: string;
  turn_id?: string;
  profile?: string;
  text?: string;
  request?: string;
  skills?: Candidate[];
  tools?: Candidate[];
  personas?: Candidate[];
  explicit_choice?: boolean;
  consume_preparation?: boolean;
  evidence?: { status?: 'success' | 'failure' | 'unknown'; tool_name?: string; wrote_files?: boolean; verify?: VerifyKind[] };
  /** Logged without calling the API: automatic notification or oversized request. */
  skip_reason?: 'automatic_notification' | 'too_large';
  /** Who sent the request: interactive human session, SDK/print mode, scheduled job, Hermes platform. */
  origin?: string;
}
export type VerifyKind = 'git' | 'http' | 'test' | 'read';
export interface Evidence {
  success: number; failure: number; unknown: number; writes: number;
  /** Local only (never sent upstream): verification kinds seen in the turn and their order. */
  verify?: Record<VerifyKind, number>; seq?: number; last_write?: number; last_verify?: number;
}
export interface CodeCheck { claims: string[]; missing: string[]; edited_after_verify: boolean; note?: string }
export interface Guidance {
  status: 'ok' | 'cached' | 'skipped' | 'fallback';
  event: string;
  turn_id: string;
  context: string;
  selection: Record<string, string | boolean>;
  observations: Record<string, number | boolean>;
  reason?: string;
  usage?: { input_tokens: number; output_tokens: number };
  ms: number;
  /** v3: numeric/enum answers for the log (no text). */
  signals?: Record<string, number | string>;
  /** v3 active questions that produced a note. */
  fired?: string[];
  /** v3 shadow questions over their study threshold (log only). */
  shadow_fired?: string[];
  /** v3 questions left out by the contract limit. */
  dropped?: string[];
  /** Version of the live calibration file in effect (calibracao-viva.json), when it has valid adjustments. */
  calibration?: string;
  /** Code check "pronto sem prova" at the end of the turn. */
  code_check?: CodeCheck;
}
export interface SessionState {
  version: number;
  day: string;
  calls: number;
  failures: number;
  circuit_until: number;
  circuit_trips?: number;
  turn_id: string;
  turn_calls: number;
  prepare_fingerprint: string;
  prepare_at: number;
  guidance: Guidance | null;
  guidance_consumed: boolean;
  evidence: Evidence;
  seen: Record<string, Guidance>;
  cache: Record<string, { at: number; result: Guidance }>;
}
export interface BuildResult { args?: Arguments; reason?: string; masked?: number; sensitive?: string; dropped?: string[]; /** versão do texto vivo das perguntas v3 aplicado */ textos?: string }
export interface AutomationOptions {
  stateDir?: string;
  client?: (args: unknown) => Promise<Result>;
  now?: () => number;
  /** Final observation call; on by default again in v3, JEV_OBSERVE_ENABLED=0 turns it off. */
  observe?: boolean;
}
