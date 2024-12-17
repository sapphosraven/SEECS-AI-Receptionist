using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using Newtonsoft.Json;

public class LipSyncController : MonoBehaviour
{
    [System.Serializable]
    public class PhonemeBlendShapeMapping
    {
        public string phoneme;
        public int blendShapeIndex;
        public float durationMultiplier;
    }

    public SkinnedMeshRenderer skinnedMeshRenderer;
    public List<PhonemeBlendShapeMapping> phonemeMappings;
    public float baseDuration = 0.1f;

    private Queue<(string phoneme, float startTime, float endTime)> phonemeQueue = new Queue<(string, float, float)>();
    private bool isAnimating = false;

    private Dictionary<string, int> visemeMap = new Dictionary<string, int>()
    {
        // Silence
        {"sil", 0},

        // Group 1: Closed mouth sounds (P, B, M)
        {"p", 1}, {"b", 1}, {"m", 1},

        // Group 2: Teeth-to-lip sounds (F, V)
        {"f", 2}, {"v", 2},

        // Group 3: Open vowels (AA, AE, AH, AO, EH, IH, EY, AY)
        {"aa", 3}, {"ae", 3}, {"ah", 3}, {"ao", 3}, {"eh", 3}, {"ih", 3}, {"ey", 3}, {"ay", 3},

        // Group 4: Wide open vowels (UW, OW, AW)
        {"uw", 4}, {"ow", 4}, {"aw", 4},

        // Group 5: Narrow vowels (EE, IY, ER, UH)
        {"ee", 5}, {"iy", 5}, {"er", 5}, {"uh", 5},

        // Group 6: "TH" sounds (TH, DH)
        {"th", 6}, {"dh", 6},

        // Group 7: Sibilants (S, Z, SH, CH, JH, ZH)
        {"s", 7}, {"z", 7}, {"sh", 7}, {"ch", 7}, {"jh", 7}, {"zh", 7},

        // Group 8: Hard sounds (K, G)
        {"k", 8}, {"g", 8},

        // Group 9: Nasal sounds (N, NG)
        {"n", 9}, {"ng", 9},

        // Group 10: Lateral sound (L)
        {"l", 10},

        // Group 11: R-colored sounds (R)
        {"r", 11},

        // Group 12: Rounded lip sounds (W)
        {"w", 12},

        // Group 13: Hissing sounds and glottals (H)
        {"h", 13}, {"hh", 13},

        // Group 14: Y sounds and other light glides (Y, OY)
        {"y", 14}, {"oy", 14}
    };

    // Updated LipSyncData class to work with phonemes and times only
    [System.Serializable]
    public class LipSyncData
    {
        public List<PhonemeTimeMarker> phoneme_time_markers; // List of phoneme time markers
    }

    // Updated PhonemeTimeMarker to remove 'word' field
    [System.Serializable]
    public class PhonemeTimeMarker
    {
        public List<string> phonemes;  // List of phonemes
        public float start_time;       // Start time for the phoneme
        public float end_time;         // End time for the phoneme
    }

    void Start()
    {
        LoadLipSyncData();
    }

    /// <summary>
    /// Loads JSON data from a file in the Resources folder.
    /// </summary>
    private void LoadLipSyncData()
    {
        // Load JSON file from Resources folder
        TextAsset jsonFile = Resources.Load<TextAsset>("phoneme_time_markers"); // File: phoneme_time_markers.json
        if (jsonFile != null)
        {
            Debug.Log("JSON file loaded successfully!");
            StartLipSyncFromJson(jsonFile.text);
        }
        else
        {
            Debug.LogError("JSON file not found in Resources folder!");
        }
    }

    /// <summary>
    /// Starts lip sync animation using JSON input.
    /// </summary>
    public void StartLipSyncFromJson(string json)
    {
        try
        {
            LipSyncData lipSyncData = JsonConvert.DeserializeObject<LipSyncData>(json);

            foreach (var marker in lipSyncData.phoneme_time_markers)
            {
                // Enqueue each phoneme with its start and end time
                foreach (var phoneme in marker.phonemes)
                {
                    phonemeQueue.Enqueue((phoneme, marker.start_time, marker.end_time));
                }
            }

            if (!isAnimating)
            {
                StartCoroutine(AnimateLipSync());
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError("Failed to parse JSON: " + e.Message);
        }
    }

    /// <summary>
    /// Animates lip sync based on phoneme data without smooth transitions.
    /// </summary>
    private IEnumerator AnimateLipSync()
    {
        isAnimating = true;

        while (phonemeQueue.Count > 0)
        {
            var phonemeData = phonemeQueue.Dequeue();
            string currentPhoneme = phonemeData.phoneme;

            // If the phoneme is not in the viseme map, assign it randomly
            if (!visemeMap.ContainsKey(currentPhoneme))
            {
                string randomPhoneme = GetRandomViseme();
                Debug.LogWarning("Unknown phoneme: " + currentPhoneme + ". Mapping to: " + randomPhoneme);
                currentPhoneme = randomPhoneme;
            }

            int blendShapeIndex = visemeMap[currentPhoneme];
            float duration = phonemeData.endTime - phonemeData.startTime;

            // Directly activate the blend shape
            skinnedMeshRenderer.SetBlendShapeWeight(blendShapeIndex, 100f);

            yield return new WaitForSeconds(duration); // Wait for the phoneme to finish

            // Directly deactivate the blend shape
            skinnedMeshRenderer.SetBlendShapeWeight(blendShapeIndex, 0f);
        }

        isAnimating = false;
    }

    // Helper method to get a random viseme key
    private string GetRandomViseme()
    {
        List<string> allPhonemes = new List<string>(visemeMap.Keys);
        int randomIndex = Random.Range(0, allPhonemes.Count);
        return allPhonemes[randomIndex];
    }
}
