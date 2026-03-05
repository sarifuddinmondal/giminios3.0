// Gemini OS 3.0 - Supabase Configuration
const SUPABASE_URL = "https://oydejwctougpjbofgadd.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95ZGVqd2N0b3VncGpib2ZnYWRkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MTQwNTMsImV4cCI6MjA4ODI5MDA1M30.HT9usJhT4FTg0iLM-17_C1byIM_8ObmoB7wXL_FpM3o";

// সুপাবেস ক্লায়েন্ট ইনিশিয়ালাইজ করা
const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// গ্লোবালি ব্যবহারের জন্য এক্সপোর্ট (অপশনাল, কিন্তু সুবিধাজনক)
window.supabaseClient = _supabase;
