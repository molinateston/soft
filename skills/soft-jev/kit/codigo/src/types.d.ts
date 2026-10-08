export type Json = null | boolean | number | string | Json[] | { [key: string]: Json };
export type Context = string | Json[] | { [key: string]: Json };
export type Question =
  | { type: 'noul'; instructions: Context; criteria?: { true?: Context; false?: Context } }
  | { type: 'choice'; instructions: Context; criteria: Record<string, Context | null> }
  | { type: 'score'; instructions: Context; criteria: Context[] };
export type Arguments = { state: Context; questions: Record<string, Question> };
export type Answer =
  | { type: 'noul'; noul: number }
  | { type: 'choice'; choice: string; probabilities: Record<string, number>; confidence: number }
  | { type: 'score'; score: number; probabilities: Record<string, number>; legend: Record<string, Context>; confidence: number };
export type Usage = { input_tokens: number; output_tokens: number };
export type Result = {
  available: boolean;
  advisory_only: true;
  answers: Record<string, Answer>;
  reason?: string;
  model?: string;
  usage?: Usage;
  ms: number;
};
