"""
Pattern Recognition Module - Network analysis and pattern detection

Features:
- Network graph construction
- Timeline analysis
- Entity relationship mapping
- Pattern visualization
- Contradiction detection
- Proper error handling
"""

import networkx as nx
import matplotlib.pyplot as plt
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import logging
from collections import defaultdict
import warnings

logger = logging.getLogger(__name__)

class PatternRecognitionError(Exception):
    """Custom exception for pattern recognition errors"""
    pass

class PatternRecognizer:
    """
    Advanced pattern recognition for research data
    """
    
    def __init__(self):
        self.graph = nx.Graph()
        self.timelines = []
        self.patterns = []
    
    def extract_entities(self, text: str) -> List[str]:
        """
        Extract named entities from text using regex patterns
        """
        try:
            if not text or not isinstance(text, str):
                return []
            
            entities = set()
            
            # Capitalized phrases (potential names, organizations, locations)
            caps_entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            entities.update(caps_entities)
            
            # Email addresses
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            entities.update(emails)
            
            # URLs
            urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)
            entities.update(urls)
            
            # Financial amounts (numbers with currency symbols)
            amounts = re.findall(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP|CHF|CNY|JPY)\b', text)
            entities.update(amounts)
            
            # Years (4-digit numbers between 1900 and 2100)
            years = re.findall(r'\b(19[0-9]{2}|20[0-9]{2})\b', text)
            entities.update(years)
            
            # Remove empty strings and return list
            return [e for e in list(entities) if e.strip()]
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return []
    
    def build_network_graph(self, sources: List[Dict[str, Any]], question: str = "") -> nx.Graph:
        """
        Build network graph from research sources with error handling
        """
        try:
            if not sources:
                logger.warning("No sources provided to build network graph")
                return nx.Graph()
            
            # Validate sources
            validated_sources = []
            for i, source in enumerate(sources):
                if not isinstance(source, dict):
                    logger.warning(f"Invalid source format at index {i}, skipping: {type(source)}")
                    continue
                validated_sources.append(source)
            
            if not validated_sources:
                logger.warning("No valid sources to build network graph")
                return nx.Graph()
            
            G = nx.Graph()
            
            # Extract entities from each source and create connections
            for source in validated_sources:
                # Get content based on source type
                if source.get('type') == 'local':
                    text = source.get('content', '')
                elif source.get('type') == 'web':
                    text = source.get('description', '') + ' ' + source.get('title', '')
                else:
                    text = str(source)
                
                if not isinstance(text, str):
                    logger.warning(f"Invalid text content in source: {source}")
                    continue
                
                entities = self.extract_entities(text)
                
                # Add nodes for entities
                for entity in entities:
                    if G.has_node(entity):
                        G.nodes[entity]['frequency'] = G.nodes[entity].get('frequency', 0) + 1
                    else:
                        G.add_node(entity, type=self._classify_entity_type(entity))
                
                # Add edges between co-occurring entities (within same source)
                for i, e1 in enumerate(entities):
                    for e2 in entities[i+1:]:
                        if G.has_edge(e1, e2):
                            G[e1][e2]['weight'] = G[e1][e2].get('weight', 0) + 1
                            sources_list = G[e1][e2].get('sources', [])
                            source_ref = source.get('file_path', source.get('url', 'unknown'))
                            if source_ref not in sources_list:
                                sources_list.append(source_ref)
                            G[e1][e2]['sources'] = sources_list
                        else:
                            source_ref = source.get('file_path', source.get('url', 'unknown'))
                            G.add_edge(e1, e2, weight=1, sources=[source_ref])
            
            # Add question-related nodes if provided
            if question and isinstance(question, str):
                question_entities = self.extract_entities(question)
                for entity in question_entities:
                    if not G.has_node(entity):
                        G.add_node(entity, type='question_entity', is_question_related=True)
            
            self.graph = G
            return G
        except Exception as e:
            logger.error(f"Error building network graph: {e}")
            return nx.Graph()
    
    def _classify_entity_type(self, entity: str) -> str:
        """
        Classify entity type based on pattern recognition
        """
        try:
            if not entity or not isinstance(entity, str):
                return 'general'
            
            # Email
            if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', entity):
                return 'email'
            
            # URL
            if re.match(r'^https?://', entity):
                return 'url'
            
            # Financial amount
            if re.match(r'^[\$€£¥]\d+', entity) or re.match(r'\d+[\s\$€£¥]', entity):
                return 'financial'
            
            # Year
            if re.match(r'^(19|20)\d{2}$', entity):
                return 'year'
            
            # Organization pattern (all caps, or common suffixes)
            if re.match(r'^[A-Z\s]+$', entity) or any(org_suffix.lower() in entity.lower() for org_suffix in ['Inc', 'LLC', 'Ltd', 'Corp', 'GmbH', 'SA']):
                return 'organization'
            
            # Person pattern (first letter caps)
            if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+', entity):
                return 'person'
            
            # Default to general
            return 'general'
        except Exception as e:
            logger.error(f"Error classifying entity type for '{entity}': {e}")
            return 'general'
    
    def analyze_network(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Analyze network properties and extract patterns with error handling
        """
        try:
            analysis = {
                'node_count': graph.number_of_nodes(),
                'edge_count': graph.number_of_edges(),
                'density': nx.density(graph) if graph.number_of_nodes() > 1 else 0,
                'centrality': {},
                'communities': {},
                'central_nodes': [],
                'entity_types': defaultdict(int)
            }
            
            if graph.number_of_nodes() == 0:
                logger.warning("Graph has no nodes to analyze")
                return analysis
            
            # Calculate centrality measures
            try:
                # Betweenness centrality (most important for information flow)
                betweenness = nx.betweenness_centrality(graph)
                analysis['centrality']['betweenness'] = betweenness
                
                # Closeness centrality
                closeness = nx.closeness_centrality(graph)
                analysis['centrality']['closeness'] = closeness
                
                # Eigenvector centrality (with error handling for disconnected graphs)
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        eigenvector = nx.eigenvector_centrality(graph, max_iter=1000, tol=1e-3)
                    analysis['centrality']['eigenvector'] = eigenvector
                except nx.NetworkXError:
                    # If eigenvector fails (e.g., disconnected graph), use degree centrality
                    degree = nx.degree_centrality(graph)
                    analysis['centrality']['degree'] = degree
                    logger.info("Eigenvector centrality failed, using degree centrality instead")
                
                # Find most central nodes
                if betweenness:
                    sorted_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
                    analysis['central_nodes'] = sorted_betweenness[:10]  # Top 10
            except Exception as e:
                logger.error(f"Error calculating centrality measures: {e}")
                # Provide basic fallback if centrality fails
                degree = dict(graph.degree())
                analysis['centrality']['degree'] = degree
                sorted_degrees = sorted(degree.items(), key=lambda x: x[1], reverse=True)
                analysis['central_nodes'] = sorted_degrees[:10]
            
            # Analyze entity types
            for node in graph.nodes():
                node_type = graph.nodes[node].get('type', 'general')
                analysis['entity_types'][node_type] += 1
            
            # Detect communities using Louvain algorithm (optional)
            try:
                import community as community_louvain  # pip install python-louvain
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    partition = community_louvain.best_partition(graph)
                analysis['communities'] = partition
            except ImportError:
                logger.info("Community detection module not available (pip install python-louvain)")
                analysis['communities'] = {}
            except Exception as e:
                logger.error(f"Error in community detection: {e}")
                analysis['communities'] = {}
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing network: {e}")
            raise PatternRecognitionError(f"Network analysis failed: {e}")
    
    def extract_timeline(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract and organize temporal information from sources
        """
        try:
            if not sources:
                logger.warning("No sources provided to extract timeline")
                return []
            
            # Validate sources
            validated_sources = []
            for i, source in enumerate(sources):
                if not isinstance(source, dict):
                    logger.warning(f"Invalid source format at index {i}, skipping: {type(source)}")
                    continue
                validated_sources.append(source)
            
            if not validated_sources:
                logger.warning("No valid sources to extract timeline")
                return []
            
            timeline_events = []
            
            # Regular expressions for date patterns
            date_patterns = [
                r'\b(\d{4})-(\d{2})-(\d{2})\b',  # YYYY-MM-DD
                r'\b(\d{2})/(\d{2})/(\d{4})\b',  # MM/DD/YYYY
                r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',  # M/D/YYYY
                r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})\b',  # Month DD, YYYY
            ]
            
            for source in validated_sources:
                content = source.get('content', '')
                if not isinstance(content, str):
                    logger.warning(f"Invalid content type in source: {type(content)}")
                    continue
                
                source_ref = source.get('file_path', source.get('url', 'unknown'))
                
                for i, pattern in enumerate(date_patterns):
                    try:
                        matches = list(re.finditer(pattern, content, re.IGNORECASE))
                        for match in matches:
                            try:
                                if i == 0:  # YYYY-MM-DD
                                    date_str = match.group(0)
                                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                                elif i == 1 or i == 2:  # MM/DD/YYYY or M/D/YYYY
                                    date_str = match.group(0)
                                    # Determine format based on match groups
                                    date_obj = datetime.strptime(date_str, 
                                        '%m/%d/%Y' if len(match.group(1)) == 2 else '%m/%d/%Y')
                                elif i == 3:  # Month DD, YYYY
                                    month = match.group(1)
                                    day = match.group(2)
                                    year = match.group(3)
                                    date_str = f"{month} {day}, {year}"
                                    date_obj = datetime.strptime(date_str, '%b %d, %Y')
                                
                                # Extract context around the date (200 chars before and after)
                                start = max(0, match.start() - 200)
                                end = min(len(content), match.end() + 200)
                                context = content[start:end].strip()
                                
                                timeline_events.append({
                                    'date': date_obj,
                                    'date_str': date_str,
                                    'source': source_ref,
                                    'context': context,
                                    'type': source.get('type', 'unknown')
                                })
                            except ValueError:
                                # Skip invalid dates
                                continue
                    except re.error as e:
                        logger.error(f"Error in regex pattern {i}: {e}")
                        continue
            
            # Sort by date
            timeline_events.sort(key=lambda x: x['date'])
            
            self.timelines = timeline_events
            return timeline_events
        except Exception as e:
            logger.error(f"Error extracting timeline: {e}")
            raise PatternRecognitionError(f"Timeline extraction failed: {e}")
    
    def generate_timeline_report(self, timeline_events: List[Dict[str, Any]]) -> str:
        """
        Generate markdown timeline report
        """
        try:
            if not timeline_events:
                return "# Timeline Analysis\n\nNo temporal patterns detected.\n"
            
            # Validate events
            validated_events = []
            for i, event in enumerate(timeline_events):
                if not isinstance(event, dict):
                    logger.warning(f"Invalid timeline event at index {i}, skipping: {type(event)}")
                    continue
                if 'date' not in event:
                    logger.warning(f"Timeline event missing date at index {i}, skipping: {event}")
                    continue
                validated_events.append(event)
            
            report = "# Timeline Analysis\n\n"
            
            for event in validated_events:
                date_str = event['date'].strftime('%Y-%m-%d') if hasattr(event['date'], 'strftime') else str(event['date'])
                report += f"## {date_str}\n"
                report += f"**Source:** {event.get('source', 'Unknown')}\n\n"
                report += f"{event.get('context', 'No context')}\n\n"
            
            return report
        except Exception as e:
            logger.error(f"Error generating timeline report: {e}")
            raise PatternRecognitionError(f"Timeline report generation failed: {e}")
    
    def detect_patterns(self, graph: nx.Graph, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect patterns in the network and sources
        """
        try:
            if graph.number_of_nodes() == 0:
                logger.info("Graph has no nodes, no patterns to detect")
                return []
            
            patterns = []
            
            # Pattern 1: High-degree nodes (hubs)
            degrees = dict(graph.degree())
            sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
            
            # Top connected nodes
            for node, degree in sorted_degrees[:5]:
                if degree > 1:  # Only if connected to others
                    patterns.append({
                        'type': 'hub',
                        'node': node,
                        'degree': degree,
                        'description': f"'{node}' connects to {degree} other entities",
                        'significance': 'central_to_network'
                    })
        
            # Pattern 2: Communities/clusters (if community detection available)
            try:
                import community as community_louvain
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    partition = community_louvain.best_partition(graph)
                
                # Analyze communities
                communities = defaultdict(list)
                for node, comm_id in partition.items():
                    communities[comm_id].append(node)
                
                for comm_id, nodes in communities.items():
                    if len(nodes) > 1:  # Only meaningful communities
                        patterns.append({
                            'type': 'community',
                            'id': comm_id,
                            'node_count': len(nodes),
                            'nodes': nodes,
                            'description': f"Community {comm_id} contains {len(nodes)} interconnected entities",
                            'significance': 'clustered_relationships'
                        })
            except ImportError:
                logger.info("Community detection not available (pip install python-louvain)")
            except Exception as e:
                logger.error(f"Error in community detection: {e}")
        
            # Pattern 3: Temporal clustering (events close in time)
            if len(self.timelines) > 1:
                # Look for events within 7 days of each other
                for i, event1 in enumerate(self.timelines):
                    for j, event2 in enumerate(self.timelines[i+1:], i+1):
                        try:
                            time_diff = abs((event1['date'] - event2['date']).days)
                            if 0 < time_diff <= 7:  # Within a week
                                patterns.append({
                                    'type': 'temporal_cluster',
                                    'events': [event1, event2],
                                    'time_diff_days': time_diff,
                                    'description': f"Events clustered within {time_diff} days of each other",
                                    'significance': 'temporal_correlation'
                                })
                        except Exception:
                            # Skip if date comparison fails
                            continue
            
            self.patterns = patterns
            return patterns
        except Exception as e:
            logger.error(f"Error detecting patterns: {e}")
            raise PatternRecognitionError(f"Pattern detection failed: {e}")
    
    def detect_contradictions(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential contradictions in sources
        """
        try:
            if len(sources) < 2:
                logger.info("Need at least 2 sources to detect contradictions")
                return []
            
            # Validate sources
            validated_sources = []
            for i, source in enumerate(sources):
                if not isinstance(source, dict):
                    logger.warning(f"Invalid source format at index {i}, skipping: {type(source)}")
                    continue
                if 'content' not in source:
                    logger.warning(f"Source at index {i} missing content, skipping: {source}")
                    continue
                validated_sources.append(source)
            
            if len(validated_sources) < 2:
                logger.info("Need at least 2 validated sources to detect contradictions")
                return []
            
            contradictions = []
            
            # Simple contradiction detection based on keywords
            contradiction_keywords = [
                ('claimed', 'denied'),
                ('true', 'false'),
                ('yes', 'no'),
                ('agreed', 'disagreed'),
                ('confirmed', 'denied'),
                ('publicly', 'privately'),
                ('officially', 'reportedly'),
                ('supported', 'opposed'),
                ('positive', 'negative'),
                ('increase', 'decrease')
            ]
            
            for i, source1 in enumerate(validated_sources):
                content1 = source1.get('content', '').lower()
                if not isinstance(content1, str):
                    continue
                
                for j, source2 in enumerate(validated_sources[i+1:], i+1):
                    content2 = source2.get('content', '').lower()
                    if not isinstance(content2, str):
                        continue
                    
                    for word1, word2 in contradiction_keywords:
                        if (word1 in content1 and word2 in content2) or (word2 in content1 and word1 in content2):
                            contradictions.append({
                                'type': 'potential_contradiction',
                                'source1': source1,
                                'source2': source2,
                                'keywords': [word1, word2],
                                'description': f"Keywords '{word1}' vs '{word2}' detected in different sources"
                            })
        
            return contradictions
        except Exception as e:
            logger.error(f"Error detecting contradictions: {e}")
            raise PatternRecognitionError(f"Contradiction detection failed: {e}")
    
    def visualize_network(self, graph: nx.Graph, output_file: str = 'network.png', 
                         figsize: Tuple[int, int] = (12, 8), 
                         node_limit: int = 100) -> Optional[str]:
        """
        Create network visualization with error handling
        """
        try:
            if graph.number_of_nodes() == 0:
                logger.warning("Graph has no nodes to visualize")
                return None
            
            # Limit node count to prevent huge plots
            if graph.number_of_nodes() > node_limit:
                logger.info(f"Graph has {graph.number_of_nodes()} nodes, limiting to {node_limit} for visualization")
                # Get most central nodes to keep
                try:
                    centrality = nx.betweenness_centrality(graph)
                    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:node_limit]
                    top_node_names = [node for node, _ in top_nodes]
                    graph = graph.subgraph(top_node_names)
                except Exception:
                    # If centrality calculation fails, just take first nodes
                    nodes = list(graph.nodes())[:node_limit]
                    graph = graph.subgraph(nodes)
            
            # Create figure with specified size
            plt.figure(figsize=figsize)
            
            # Position nodes using spring layout
            pos = nx.spring_layout(graph, k=0.5, iterations=50)
            
            # Node sizes based on centrality (if computed)
            try:
                node_centralities = nx.betweenness_centrality(graph)
                node_sizes = [1000 * (node_centralities.get(node, 0.1) + 0.1) for node in graph.nodes()]
            except:
                # If centrality fails, use degree
                degrees = dict(graph.degree())
                node_sizes = [1000 * (degrees.get(node, 0.1) + 0.1) for node in graph.nodes()]
            
            # Node colors based on type
            node_colors = []
            for node in graph.nodes():
                node_type = graph.nodes[node].get('type', 'general')
                color_map = {
                    'person': 'lightblue',
                    'organization': 'lightgreen',
                    'url': 'orange',
                    'financial': 'gold',
                    'year': 'pink',
                    'email': 'lightcoral',
                    'general': 'lightgray'
                }
                node_colors.append(color_map.get(node_type, 'lightgray'))
            
            # Draw network
            nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.7)
            nx.draw_networkx_labels(graph, pos, font_size=8, font_weight='bold')
            
            # Draw edges with width based on weight
            if graph.number_of_edges() > 0:
                edges = graph.edges()
                weights = []
                for u, v in edges:
                    weight = graph[u][v].get('weight', 1)
                    weights.append(weight)
                
                if weights:
                    max_weight = max(weights) if weights else 1
                    edge_widths = [2 * (w / max_weight) for w in weights]  # Normalize to 1-2 range
                    nx.draw_networkx_edges(graph, pos, width=edge_widths, alpha=0.5)
            
            plt.title("Entity Relationship Network")
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Network visualization saved to: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error creating network visualization: {e}")
            return None

# Example usage:
# recognizer = PatternRecognizer()
# graph = recognizer.build_network_graph(sources)
# analysis = recognizer.analyze_network(graph)
# timeline = recognizer.extract_timeline(sources)
# patterns = recognizer.detect_patterns(graph, sources)
# recognizer.visualize_network(graph, 'output.png')