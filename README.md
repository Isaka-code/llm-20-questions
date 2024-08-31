# 9th Place Solution - [LLM 20 Questions](https://www.kaggle.com/competitions/llm-20-questions)

## 1. Introduction
First and foremost, I would like to express my gratitude to the organizers, the Kaggle team, and all the participants. The familiar theme of the 20 Questions game made this competition particularly enjoyable to work on! Despite the task's relatively high implementation complexity, I managed to effectively develop it by splitting it into more than ten loosely coupled Python scripts and creating nearly a hundred test cases.

This solution integrates rule-based logic, keyword matching, and LLM context-based responses to achieve a high level of accuracy in identifying keywords.

This solution achieved a public score of 1023.5 (highest) , securing 3rd place. The score was achieved with three wins as a guesser (Agent Alpha victories not included) , zero losses, and three draws. In a similar subsequent submission, it scored 982.9, remaining within the gold medal range, with three wins as a guesser (Agent Alpha victories not included) and one win as an answerer, consistently reaching the gold medal range.

![public 3rd Place](https://github.com/Isaka-code/llm-20-questions/blob/main/images/public_3rd_place.png)

A few days before the evaluation period with the private keyword set ended, I reached a peak of 2nd place (with only a 0.7-point difference from 1st place, practically a margin of error). In the end, I finished 9th, but I’m very satisfied with earning a solo gold medal!


![private 9th Place](https://github.com/Isaka-code/llm-20-questions/blob/main/images/final_private_LB.png)


## 2. Answer Agent
I combined the following Answer agents, prioritized in the order of 1, 2, 3, and 4:
1. **Rule-based Yes/No responses when matching specific protocols**:
   - This method was responsible for approximately 15% of the Answers.
   - All protocols identified from episodes were managed effectively.
   - Ultimately, 23 types of protocols were included.
   - To minimize implementation errors, I created multiple test cases for each protocol.
   - The implementation was generalized to handle variations in uppercase, lowercase, double quotes, single quotes, and the absence of quotes.
2. **Pre-defined keyword-question pairs**:
   - This method was responsible for approximately 5% of the Answers.
   - If a keyword-question pair matched the pre-defined matrix, the corresponding answer was deemed appropriate.
   - Keywords and questions were pre-processed using `.lower().strip()`.
   - When this method was enabled, the success rate for self-play with most keywords was nearly 100%. This suggests that when the values of the Answer and Ask/Guess agents align perfectly, it is easy to arrive at the correct keyword. The discrepancy in values is what contributes to the task's difficulty. Despite the Answer agent being underrated compared to the Ask/Guess agents, the reduction factor(proposed in [this discussion](https://www.kaggle.com/competitions/llm-20-questions/discussion/520021)) for each round, raised to the power of 20, creates significant differences.


![N=1 per reduction_factor ^ 20](https://github.com/Isaka-code/llm-20-questions/blob/main/images/N%3D1%20per%20reduction_factor%20%5E%2020.png)





3. **LLM + Wikipedia Context-based responses**:
   - This method was responsible for approximately 80% of the Answers.
   - I used llama3.1-8B-IT with parameters: `do_sample=False`, `max_tokens=1`, and `bad_words_ids=["maybe", "Maybe", "none", "None", "Invalid", "invalid", "INVALID", "I", "can", "can't", "Can't", "CAN'T", "I'm", "I'll", "I've"]`. [The shared system prompt](https://www.kaggle.com/competitions/llm-20-questions/discussion/524258) was configured accordingly.
   - The secret keyword was compared with titles from a pre-prepared Wikipedia dataset to retrieve relevant text, thereby extending the LLM's knowledge base and improving the CV score from 17.1 % to 31.4 %.
   - Wikipedia titles were compared only up to the first parenthesis.
     - Priority 1: Exact match
     - Priority 2: Case-insensitive match using `.lower().strip()`
     - Priority 3: Normalized match using the competition's GitHub comparison function
   - Context length restrictions:
     - Texts under 280 characters were not used.
     - Texts over 2048 characters were truncated at a natural point.
4. **Exception handling**:
   - This method was responsible for approximately 0% of the Answers.
   - Added exception handling for errors or issues in steps 1, 2, and 3.
   - In case of exceptions, "no" was selected as the response since it is statistically more likely to occur than "yes".

## 3. Asker/Guesser Flow
In Round 1, the question 'Is it Agent Alpha?' is posed. If the answer is No, follow these steps:

### Asker Step
1. Set up a highest score keyword set.
2. Calculate E (a metric related to the expected reduction in candidate keywords) for each question and select the question with the highest E.
3. Remove the selected question from the question set.

### Guesser Step
1. Obtain the Answer.
2. Update the scores for the keyword set.
3. Select the keyword with the highest score.
4. Remove the selected keyword from the keyword set.

Repeat until the round limit is reached.

## 4. Asker Agent
### 4.1. Question principles:
1. **Clarity**: Questions should reliably elicit stable Yes/No answers regardless of the Answer. Verified by asking the LLM the same question and checking for consistent responses. Adjusted temperature and parameters for further stability evaluation. Clarity was prioritized over a hard semantic binary search, opting instead for a soft search of top answer candidates.
2. **Independence**: Questions with high independence were preferred, determined by Yes/No correlation coefficients. Redundant questions were excluded by focusing on keywords with split opinions and evaluating clarity.
3. **High Information Gain**: A question like "Is it an Asian country?" provides more information than "Is it in the Baltic States?" However, as rounds progress and keyword candidates narrow, this principle adjusts. Generally, the reduction factor for p(ratio of yes in total) is p^2 + (1-p)^2, minimized at p=0.5. In my observations, past popular questions like 'Is it a place?' have a p value closer to 0.33, rather than the expected 0.25.

These principles were also applied to an algorithm designed to select questions with high information gain from a pre-prepared keyword-question matrix. Even if a question has high information gain, if it lacks clarity, it is not selected. Therefore, an additional "Tie" option was introduced to factor in clarity when choosing questions. Instead of simply selecting questions with a p value close to 0.5, the algorithm calculates E and selects the question with the highest E.

![Formulas](https://github.com/Isaka-code/llm-20-questions/blob/main/images/Formulas.png)




Here is the explanation of E:
- **y, n, t**: These represent the total number of 'yes', 'no', and 'tie' responses for a given question.
- The first and second terms correspond to the expected number of keyword candidates that will be eliminated by a question with the counts y, n, and t.
- The third and fourth terms serve as tiebreakers. Thanks to the terms, if the expected values are the same, the question with fewer 't' responses and with more 'y' responses will be chosen (assuming that 'no' responses generally outnumber 'yes' responses).

## 5. Guesser Agent
1. Using the simple method of maintaining consistency between keywords and pre-determined Yes/No answers often exhausts keyword candidates by Round 10. This discrepancy arises from differences between pre-determined and actual answers. To buffer this, a scoring system was introduced.
2. Scores are calculated for each keyword, with the highest score chosen each round.
3. Initial scores are set by tier.
4. Scores are adjusted based on consistency with Answers, with Yes/No matches increasing scores by 1. If a keyword answer is Tie, its score is not updated, avoiding unnecessary adjustments.


![simulated_scores](https://github.com/Isaka-code/llm-20-questions/blob/main/images/simulated_scores.png)




## 6. When Agent Alpha is Effective
If "Is it Agent Alpha?" yields a Yes in Round 1, fall back to a binary search approach using the following steps:
1. Prepare primary keyword candidates (2,046) and supplementary keyword candidates (~100,000).
2. Steps:
   - Binary search with primary keywords.
   - Binary search with supplementary keywords using the information gathered.
   - If not found, fall back to the standard approach, assuming the pair bot  is a false Agent Alpha.
3. Primary keyword candidates are set to 2046 to exhaust the search in exactly 10 turns.
(2046->1022->510->254->126->62->30->14->6->2->0)
4. Dividing keywords into primary and supplementary sets increases the chances of winning in mirror matches against Agent Alpha, while still allowing success against other opponents around Round 17.

### By the way, Should You Use Agent Alpha?
I thought the pros outweighed the cons.
**Pros:**
- High success rate in identifying keywords.
- Not dependent on the responder's yes/no perspectives.
- Effective for escaping low-rating ranges.

**Cons:**
- Consumes one turn.
- Often suffers significant losses against false Agent Alpha pair bots.
- Requires preparing keyword candidates.

## 7. Creating the Dataset
Like many other LLM competitions, dataset creation was a key factor in this competition. I followed these steps:

### Keyword Collection:
- Sample 10 keywords from the public 'Things' category. Use the LLM to iteratively generate 30 new keywords, continuing until no new keywords are produced.
- Added all keyword datasets shared in discussions.
- Used LLM to determine if English Wikipedia titles belong to the "Things" category (limited to binary search due to high false positives).
- Manually added all keywords that came to mind.

Below is the Embedding representations of Public keywords and Tier 1 keywords (the highest quality dataset among the generated keywords).

![Semantic Visualization of Keywords with LLama3.1 Embeddings](https://github.com/Isaka-code/llm-20-questions/blob/main/images/Semantic%20Visualization%20of%20Keywords%20with%20LLama3.1%20Embeddings.png)




### Question Collection:
**Collection**:
- Gather questions from episodes of top Kagglers on the leaderboard.
- Use shared datasets from [here](https://www.kaggle.com/code/khahuras/offline-policy-questioner-agent).
- Manually add questions that seem missing types of questions.
  - My favorite question is `len(keyword.split()) == 2? # Is the length of the keyword two words?`. I think it’s excellent in terms of Clarity, Independence, and High Information Gain.

**Removal**:
- Remove questions lacking clarity or having high correlation with others.
- Finalized 521 questions, deemed sufficient for pre-evaluation.

### Answer Creation:
- Use LLM to create Yes/No answers, including Tie responses.
  - I initially used different temperatures for diverse answers. However, I modified the prompt to include "unsure" and "irrelevant" for Tie answers in a single inference.
- Generated a final dataset with 15,113 keywords and 521 questions.
  - Created a similar dataset for 1,497 public keywords for initial algorithm development, used for CV and leaderboard validation.

Below are the counts of yes, no, and tie responses for each of the 1,497 public keywords (not whole questions included):


![the counts of yes, no, and tie responses for each of the 1,497 public keywords (not whole questions included)](https://github.com/Isaka-code/llm-20-questions/blob/main/images/the%20counts%20of%20yes%2C%20no%2C%20and%20tie%20responses%20for%20each%20of%20the%201%2C497%20public%20keywords%20(not%20whole%20questions%20included).png)




### Dataset Sorting:
- Questions were ordered by the E in their initial values.
- Keywords dataset split into Tier 1, 2, 3, and 4 to avoid reliance on a single dataset.
  - You can check the definition of the Tier is [here](https://www.kaggle.com/datasets/isakatsuyoshi/llm-20-questions-keyword-question-mapping)
  - Initial score 0.0 for Tier1, -0.5 for Tier2, -1.0 for Tier3 and -1.5 for Tier4
  - Until Round 11, Tier 1 questions mainly targeted .
  - Later rounds involve a dynamic exchange among top-scoring questions from all tiers, naturally expanding the dataset.

**Final Submissions**:
I selected final submissions for the diversity:
- Submission ①: Tiers 1, 2, 3, 4
- Submission ②: Tiers 1+2 (Tier 2 treated as Tier 1), and Tiers 3, 4.


## 8. Sharing Source Code and Datasets

I'm happy to share the source code (on Kaggle, GitHub), test code, and datasets!

### 8.1 Source Code
**Kaggle**
- [Final Submission - LLM 20 Questions](https://www.kaggle.com/code/isakatsuyoshi/final-submission-llm-20-questions): Final submission notebook
- [Llama 3.1 · 8b-instruct Fix Json](https://www.kaggle.com/code/isakatsuyoshi/llama-3-1-8b-instruct-fix-json): This allows Llama 3.1-8B-IT to be used in the Kaggle environment (see the reference discussion [here](https://www.kaggle.com/competitions/llm-20-questions/discussion/523619))
- [Semantic Visualization of Keywords](https://www.kaggle.com/code/isakatsuyoshi/semantic-visualization-of-keywords): Visualizes the keyword embeddings using UMAP after dimensionality reduction with Llama 3.1-8B-IT
- [Theoretical Analysis of the 20 Questions Game](https://www.kaggle.com/competitions/llm-20-questions/discussion/520021): Discussion on simulating the reduction factor for each round of the 20 Questions game (with source code included)

**GitHub**

[GitHub Repository Link](https://github.com/Isaka-code/llm-20-questions)


- src/llm20_main.py: The main script that serves as the entry point
- src/llm20_config.py: Class for setting parameters
- src/logger.py: Class for logging
- src/robot.py: Class for selecting algorithms
- src/keyword_question_mapping.py: Class for mapping keywords to questions
- src/formulas.py: Formula for calculating E
- src/dictionary_binary_search.py: Class for performing dictionary binary search
- src/llm20_llm_system.py: Class related to the LLM system
- src/wiki_data.py: Class for handling the Wikipedia dataset
- src/protocol.py: Script for handling protocols found in episodes using rule-based methods
- src/word_utils.py: Scripts including the official competition normalization functions
- src/simulate_score.py: Script for simulating score transitions
- tests/: Directory containing test codes for the scripts mentioned above

### 8.2 Datasets
- [LLM 20 Questions - Wikipedia Context](https://www.kaggle.com/datasets/isakatsuyoshi/llm-20-questions-wikipedia-context)
- [LLM 20 Questions - Dictionary Binary Search](https://www.kaggle.com/datasets/isakatsuyoshi/llm-20-questions-dictionary-binary-search)
- [LLM 20 Questions - Keyword Question Mapping](https://www.kaggle.com/datasets/isakatsuyoshi/llm-20-questions-keyword-question-mapping)
- [EDA of LLM 20 Questions Solution Datasets](https://www.kaggle.com/code/isakatsuyoshi/nth-place-eda-of-the-datasets): This notebook presents an Exploratory Data Analysis (EDA) of the three datasets
