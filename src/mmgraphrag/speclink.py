"""SpecLink: Spectral Clustering-Based Cross-Modal Entity Linking (CMEL).
Implements the algorithm from Section 3.3.1 and Appendix H.3 of Wan & Yu (arXiv:2507.20804v3).
"""

import math
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SpecLinkAligner:
    """Spectral Clustering-based cross-modal entity alignment engine."""

    def __init__(self, dbscan_eps: float = 0.5, alignment_threshold: float = 0.55):
        self.eps = dbscan_eps
        self.threshold = alignment_threshold

    def _compute_embeddings(self, texts: List[str]) -> np.ndarray:
        """Computes normalized semantic embeddings using character/word n-gram TF-IDF vectorizer."""
        if not texts:
            return np.zeros((0, 32))
        vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
        emb = vectorizer.fit_transform(texts).toarray()
        # L2 normalize
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return emb / norms

    def run_speclink_clustering(
        self,
        text_entities: List[str],
        relation_weights: Optional[Dict[Tuple[str, str], float]] = None
    ) -> List[List[str]]:
        """Executes SpecLink Spectral Clustering (L = D - A + DBSCAN) on candidate textual entities."""
        n = len(text_entities)
        if n == 0:
            return []
        if n == 1:
            return [text_entities]

        relation_weights = relation_weights or {}

        # 1. Compute pairwise semantic similarity
        V = self._compute_embeddings(text_entities)
        sim_matrix = np.clip(cosine_similarity(V), 0.0, 1.0)

        # 2. Build Reweighted Adjacency Matrix: A_pq = sim(v_p, v_q) * weight(r_pq)
        A = np.zeros((n, n), dtype=float)
        for p in range(n):
            for q in range(n):
                if p == q:
                    A[p, q] = 0.0
                    continue
                w = relation_weights.get((text_entities[p], text_entities[q]), 1.0)
                A[p, q] = sim_matrix[p, q] * w

        # Symmetrize
        A = np.maximum(A, A.T)

        # 3. Compute Degree Matrix D and Laplacian L = D - A
        D = np.diag(np.sum(A, axis=1))
        L = D - A

        # 4. Eigen-decomposition and spectral coordinates Q
        m = max(2, int(math.ceil(math.sqrt(n))))
        m = min(m, n)
        eigenvalues, eigenvectors = np.linalg.eigh(L)
        # Select smallest m eigenvectors
        idx = np.argsort(eigenvalues)[:m]
        Q = eigenvectors[:, idx]

        # 5. Cluster row space of Q with DBSCAN
        min_samples = max(1, int(math.ceil(n / 10.0)))
        dbscan = DBSCAN(eps=self.eps, min_samples=min_samples, metric="euclidean")
        labels = dbscan.fit_predict(Q)

        # 6. Group entities into clusters
        clusters: Dict[int, List[str]] = {}
        for ent, label in zip(text_entities, labels):
            clusters.setdefault(label, []).append(ent)

        return list(clusters.values())

    def align_visual_entity(
        self,
        visual_entity: str,
        text_entities: List[str],
        relation_weights: Optional[Dict[Tuple[str, str], float]] = None
    ) -> Optional[Tuple[str, float]]:
        """Aligns a visual entity to the best matching textual entity using SpecLink clustering."""
        if not text_entities:
            return None

        # 1. Run Spectral Clustering on candidate text entities
        clusters = self.run_speclink_clustering(text_entities, relation_weights)
        if not clusters:
            return None

        # 2. Embed visual entity and all text entities
        all_texts = [visual_entity] + text_entities
        embeddings = self._compute_embeddings(all_texts)
        v_img = embeddings[0:1]
        v_texts = embeddings[1:]

        text_to_idx = {t: idx for idx, t in enumerate(text_entities)}

        # 3. Find most relevant cluster via nearest-neighbor cosine similarity
        best_cluster = None
        best_cluster_sim = -1.0
        for cluster in clusters:
            cluster_indices = [text_to_idx[t] for t in cluster if t in text_to_idx]
            if not cluster_indices:
                continue
            cluster_sims = cosine_similarity(v_img, v_texts[cluster_indices])
            max_sim = float(np.max(cluster_sims))
            if max_sim > best_cluster_sim:
                best_cluster_sim = max_sim
                best_cluster = cluster

        if not best_cluster:
            return None

        # 4. Select best candidate entity within the selected cluster
        best_entity = None
        highest_sim = -1.0
        for cand in best_cluster:
            cand_idx = text_to_idx[cand]
            sim = float(cosine_similarity(v_img, v_texts[cand_idx:cand_idx+1])[0, 0])
            if sim > highest_sim:
                highest_sim = sim
                best_entity = cand

        if highest_sim >= self.threshold and best_entity:
            return best_entity, round(highest_sim, 4)

        return None
