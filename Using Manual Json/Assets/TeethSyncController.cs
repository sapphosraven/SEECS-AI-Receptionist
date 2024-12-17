using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;

public class TeethSyncController : MonoBehaviour
{
    [System.Serializable]
    public class PhonemeBlendShapeMapping
    {
        public string phoneme;
        public int blendShapeIndex;
        public float durationMultiplier;
    }

    public SkinnedMeshRenderer skinnedMeshRenderer;  // Reference to the Teeth SkinnedMeshRenderer
    public List<PhonemeBlendShapeMapping> phonemeMappings;
    public float baseDuration = 0.1f;

    private Queue<(string phoneme, float startTime, float endTime)> phonemeQueue = new Queue<(string, float, float)>();
    private bool isAnimating = false;

    private Dictionary<string, int> visemeMap = new Dictionary<string, int>()
    {
        // Same phoneme-to-viseme mappings as in Wolf3D_Head
        {"sil", 0},
        {"p", 1}, {"b", 1}, {"m", 1},
        {"f", 2}, {"v", 2},
        {"aa", 3}, {"ae", 3}, {"ah", 3}, {"ao", 3}, {"eh", 3}, {"ih", 3}, {"ey", 3}, {"ay", 3},
        {"uw", 4}, {"ow", 4}, {"aw", 4},
        {"ee", 5}, {"iy", 5}, {"er", 5}, {"uh", 5},
        {"th", 6}, {"dh", 6},
        {"s", 7}, {"z", 7}, {"sh", 7}, {"ch", 7}, {"jh", 7}, {"zh", 7},
        {"k", 8}, {"g", 8},
        {"n", 9}, {"ng", 9},
        {"l", 10},
        {"r", 11},
        {"w", 12},
        {"h", 13}, {"hh", 13},
        {"y", 14}, {"oy", 14}
    };

    [System.Serializable]
    public class LipSyncData
    {
        public List<PhonemeTimeMarker> phoneme_time_markers;
    }

    [System.Serializable]
    public class PhonemeTimeMarker
    {
        public List<string> phonemes;  // List of phonemes
        public float start_time;
        public float end_time;
    }

    void Start()
    {
        LoadLipSyncData();
    }

    private void LoadLipSyncData()
    {
        TextAsset jsonFile = Resources.Load<TextAsset>("phoneme_time_markers");
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

    public void StartLipSyncFromJson(string json)
    {
        try
        {
            LipSyncData lipSyncData = JsonConvert.DeserializeObject<LipSyncData>(json);

            foreach (var marker in lipSyncData.phoneme_time_markers)
            {
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

    private IEnumerator AnimateLipSync()
    {
        isAnimating = true;

        while (phonemeQueue.Count > 0)
        {
            var phonemeData = phonemeQueue.Dequeue();
            string currentPhoneme = phonemeData.phoneme;

            if (visemeMap.ContainsKey(currentPhoneme))
            {
                int blendShapeIndex = visemeMap[currentPhoneme];
                skinnedMeshRenderer.SetBlendShapeWeight(blendShapeIndex, 100f);

                float duration = phonemeData.endTime - phonemeData.startTime;
                yield return new WaitForSeconds(duration);

                skinnedMeshRenderer.SetBlendShapeWeight(blendShapeIndex, 0f);
            }
            else
            {
                Debug.LogWarning("Unknown phoneme: " + currentPhoneme);
                yield return null;
            }
        }

        isAnimating = false;
    }
}
