-- 1. Activate the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Drop existing tables if they exist to allow clean resets
DROP TABLE IF EXISTS public.face_embeddings CASCADE;
DROP TABLE IF EXISTS public.persons CASCADE;

-- 3. Create the core identities table
CREATE TABLE public.persons (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create the facial vectors table with the JSONB context column
CREATE TABLE public.face_embeddings (
    embedding_id SERIAL PRIMARY KEY,
    person_id INT REFERENCES public.persons(person_id) ON DELETE CASCADE,
    embedding vector(512) NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Build the high-speed HNSW index for millisecond vector lookups
CREATE INDEX IF NOT EXISTS face_embeddings_hnsw_idx 
ON public.face_embeddings USING hnsw (embedding vector_cosine_ops);