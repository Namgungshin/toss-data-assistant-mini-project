-- Toss AI Platform Data Assistant mini project
-- Assumption: label metadata is loaded into a table named label_metadata.
-- This SQL intentionally excludes raw consulting text, question, answer, and output fields.

-- 1. Domain distribution
SELECT
  consulting_category,
  COUNT(*) AS row_count
FROM label_metadata
GROUP BY consulting_category
ORDER BY row_count DESC;

-- 2. Train/validation distribution
SELECT
  split,
  consulting_category,
  COUNT(*) AS row_count
FROM label_metadata
GROUP BY split, consulting_category
ORDER BY split, row_count DESC;

-- 3. Task category distribution
SELECT
  task_category,
  COUNT(*) AS row_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ratio_pct
FROM label_metadata
GROUP BY task_category
ORDER BY row_count DESC;

-- 4. Consulting situation distribution
SELECT
  consulting_situation,
  COUNT(*) AS row_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ratio_pct
FROM label_metadata
GROUP BY consulting_situation
ORDER BY row_count DESC;

-- 5. High-volume topic candidates
SELECT
  consulting_topic,
  COUNT(*) AS row_count
FROM label_metadata
GROUP BY consulting_topic
ORDER BY row_count DESC
LIMIT 20;

-- 6. Potential review queue by sensitive financial terms
SELECT
  consulting_category,
  consulting_situation,
  core_financial_terms,
  COUNT(*) AS row_count
FROM label_metadata
WHERE core_financial_terms LIKE '%인증%'
   OR core_financial_terms LIKE '%계좌%'
   OR core_financial_terms LIKE '%비밀번호%'
   OR core_financial_terms LIKE '%카드%'
   OR core_financial_terms LIKE '%명의%'
   OR core_financial_terms LIKE '%대출%'
GROUP BY consulting_category, consulting_situation, core_financial_terms
ORDER BY row_count DESC;

-- 7. Missing label field check
SELECT
  SUM(CASE WHEN consulting_category IS NULL THEN 1 ELSE 0 END) AS missing_consulting_category,
  SUM(CASE WHEN consulting_topic IS NULL THEN 1 ELSE 0 END) AS missing_consulting_topic,
  SUM(CASE WHEN task_category IS NULL THEN 1 ELSE 0 END) AS missing_task_category,
  SUM(CASE WHEN consulting_situation IS NULL THEN 1 ELSE 0 END) AS missing_consulting_situation,
  SUM(CASE WHEN qa_topic IS NULL THEN 1 ELSE 0 END) AS missing_qa_topic,
  SUM(CASE WHEN consulting_purpose IS NULL THEN 1 ELSE 0 END) AS missing_consulting_purpose
FROM label_metadata;

-- 8. Multiple QA rows per source_id
SELECT
  split,
  domain,
  source_id,
  COUNT(*) AS qa_count
FROM label_metadata
GROUP BY split, domain, source_id
HAVING COUNT(*) > 1
ORDER BY qa_count DESC, source_id
LIMIT 50;

-- 9. Review-priority situation/topic matrix
SELECT
  consulting_situation,
  qa_topic,
  COUNT(*) AS row_count
FROM label_metadata
GROUP BY consulting_situation, qa_topic
ORDER BY
  CASE consulting_situation
    WHEN '민원응대' THEN 1
    WHEN '업무처리' THEN 2
    ELSE 3
  END,
  row_count DESC;
