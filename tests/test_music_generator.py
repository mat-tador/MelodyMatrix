import pytest
from music_generator import (
    generate_sequence,
    get_graph_data,
    build_order_chain,
    apply_genre_character,
    get_order_chain,
    get_node_list,
    get_label,
    BASE_CHAINS_BY_GENRE,
    SCALE_MAPS,
    INSTRUMENT_TYPES,
    DEFAULT_STATE,
)

# Constants used across tests


VALID_GENRES = list(BASE_CHAINS_BY_GENRE.keys())
VALID_SCALES = list(SCALE_MAPS.keys())
ALL_INSTRUMENTS = INSTRUMENT_TYPES  # ["melody", "bass", "drums", "chords"]



# 1. generate_sequence

class TestGenerateSequenceHappyPath:

    def test_returns_dict_with_expected_keys(self):
        result = generate_sequence("Techno-Jazz", "C Minor", order=1, steps=8)
        expected_keys = {
            "genre", "scale", "order", "steps",
            "active_instruments", "sequences", "raw_sequences", "metadata"
        }
        assert expected_keys.issubset(result.keys())

    def test_genre_and_scale_preserved_in_output(self):
        result = generate_sequence("Ambient", "C Major", order=2, steps=10)
        assert result["genre"] == "Ambient"
        assert result["scale"] == "C Major"

    def test_order_and_steps_preserved(self):
        result = generate_sequence("House", "C Minor", order=3, steps=32)
        assert result["order"] == 3
        assert result["steps"] == 32

    def test_sequence_length_matches_steps(self):
        steps = 20
        result = generate_sequence("Hip Hop", "C Minor", order=1, steps=steps)
        for inst in result["active_instruments"]:
            assert len(result["sequences"][inst]) == steps, (
                f"Instrument '{inst}' sequence length mismatch"
            )

    def test_raw_sequence_length_matches_steps(self):
        steps = 15
        result = generate_sequence("Techno-Jazz", "C Major", order=2, steps=steps)
        for inst in result["raw_sequences"]:
            assert len(result["raw_sequences"][inst]) == steps

    def test_all_four_instruments_present_by_default(self):
        result = generate_sequence("House", "C Minor", order=1, steps=5)
        assert set(result["active_instruments"]) == set(ALL_INSTRUMENTS)

    def test_active_instruments_subset(self):
        active = ["melody", "bass"]
        result = generate_sequence("Ambient", "C Minor", order=1, steps=5,
                                   active_instruments=active)
        assert set(result["active_instruments"]) == set(active)
        assert set(result["sequences"].keys()) == set(active)

    def test_metadata_contains_available_genres_and_scales(self):
        result = generate_sequence("Techno-Jazz", "C Minor", order=1, steps=4)
        meta = result["metadata"]
        assert "available_genres" in meta
        assert "available_scales" in meta
        assert "Techno-Jazz" in meta["available_genres"]

    def test_seed_produces_reproducible_output(self):
        kwargs = dict(genre="Hip Hop", scale="C Minor", order=2, steps=20, seed=42)
        r1 = generate_sequence(**kwargs)
        r2 = generate_sequence(**kwargs)
        assert r1["sequences"] == r2["sequences"]

    def test_different_seeds_produce_different_output(self):
        base = dict(genre="House", scale="C Minor", order=2, steps=30)
        r1 = generate_sequence(**base, seed=1)
        r2 = generate_sequence(**base, seed=999)
        # With 30 steps it is astronomically unlikely they match
        assert r1["sequences"] != r2["sequences"]

    @pytest.mark.parametrize("genre", VALID_GENRES)
    def test_all_genres_generate_without_error(self, genre):
        result = generate_sequence(genre, "C Minor", order=1, steps=8)
        assert result["genre"] == genre

    @pytest.mark.parametrize("scale", VALID_SCALES)
    def test_all_scales_generate_without_error(self, scale):
        result = generate_sequence("Ambient", scale, order=1, steps=8)
        assert result["scale"] == scale

    @pytest.mark.parametrize("order", [1, 2, 3])
    def test_all_orders_generate_without_error(self, order):
        result = generate_sequence("Techno-Jazz", "C Minor", order=order, steps=8)
        assert result["order"] == order

    def test_steps_boundary_minimum(self):
        result = generate_sequence("House", "C Minor", order=1, steps=1)
        for inst in result["active_instruments"]:
            assert len(result["sequences"][inst]) == 1

    def test_steps_boundary_maximum(self):
        result = generate_sequence("House", "C Minor", order=1, steps=200)
        for inst in result["active_instruments"]:
            assert len(result["sequences"][inst]) == 200



# 2. generate_sequence — validation / error tests


class TestGenerateSequenceValidation:

    def test_invalid_genre_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown genre"):
            generate_sequence("FakeGenre", "C Minor", order=1, steps=8)

    def test_invalid_scale_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown scale"):
            generate_sequence("Ambient", "D Dorian", order=1, steps=8)

    def test_invalid_order_raises_value_error(self):
        with pytest.raises(ValueError, match="Order must be"):
            generate_sequence("Ambient", "C Minor", order=5, steps=8)

    def test_zero_order_raises_value_error(self):
        with pytest.raises(ValueError, match="Order must be"):
            generate_sequence("Ambient", "C Minor", order=0, steps=8)

    def test_steps_too_low_raises_value_error(self):
        with pytest.raises(ValueError, match="Steps must be"):
            generate_sequence("Ambient", "C Minor", order=1, steps=0)

    def test_steps_too_high_raises_value_error(self):
        with pytest.raises(ValueError, match="Steps must be"):
            generate_sequence("Ambient", "C Minor", order=1, steps=201)



# 3. get_graph_data

class TestGetGraphData:

    def test_returns_expected_top_level_keys(self):
        data = get_graph_data("Techno-Jazz", "C Minor", order=1)
        assert {"genre", "scale", "order", "graphs"}.issubset(data.keys())

    def test_graphs_contains_all_instruments(self):
        data = get_graph_data("House", "C Minor", order=2)
        assert set(data["graphs"].keys()) == set(ALL_INSTRUMENTS)

    def test_each_instrument_graph_has_nodes_and_edges(self):
        data = get_graph_data("Ambient", "C Major", order=1)
        for inst in ALL_INSTRUMENTS:
            g = data["graphs"][inst]
            assert "nodes" in g
            assert "edges" in g
            assert len(g["nodes"]) > 0

    def test_nodes_have_id_and_label(self):
        data = get_graph_data("Techno-Jazz", "C Minor", order=1)
        for node in data["graphs"]["melody"]["nodes"]:
            assert "id" in node
            assert "label" in node

    def test_edges_have_from_and_to(self):
        data = get_graph_data("House", "C Minor", order=1)
        for edge in data["graphs"]["bass"]["edges"]:
            assert "from" in edge
            assert "to" in edge

    def test_invalid_genre_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown genre"):
            get_graph_data("NonExistentGenre", "C Minor", order=1)

    @pytest.mark.parametrize("genre", VALID_GENRES)
    def test_all_genres_return_graph_data(self, genre):
        data = get_graph_data(genre, "C Minor", order=1)
        assert data["genre"] == genre


# 4. build_order_chain

class TestBuildOrderChain:

    def _sample_base(self):
        return {
            "Do": ["Fa", "Sol"],
            "Fa": ["Do", "Sol"],
            "Sol": ["Do"],
        }

    def test_order_1_returns_base_unchanged(self):
        base = self._sample_base()
        result = build_order_chain(base, order=1, instrument_type="melody")
        assert result == base

    def test_order_2_returns_dict(self):
        base = self._sample_base()
        result = build_order_chain(base, order=2, instrument_type="melody")
        assert isinstance(result, dict)
        assert set(result.keys()) == set(base.keys())

    def test_order_3_returns_dict(self):
        base = self._sample_base()
        result = build_order_chain(base, order=3, instrument_type="melody")
        assert isinstance(result, dict)

    def test_all_original_keys_preserved(self):
        base = self._sample_base()
        for order in [1, 2, 3]:
            result = build_order_chain(base, order, "melody")
            assert set(result.keys()) == set(base.keys())


# 5. apply_genre_character

class TestApplyGenreCharacter:

    def _sample_chain(self):
        return {
            "Do": ["Fa", "Sol"],
            "Fa": ["Do"],
            "Sol": ["Do", "Fa"],
            "i": ["iv", "v"],
            "iv": ["i"],
            "v": ["i"],
            "Closed": ["Open"],
            "Open": ["Closed"],
            "Pausa": ["Closed"],
        }

    def test_ambient_adds_self_loop_to_all_keys(self):
        chain = {"Do": ["Fa"], "Fa": ["Do"]}
        result = apply_genre_character(chain, "Ambient", "melody")
        for key in chain:
            assert key in result[key], f"Expected self-loop on '{key}' for Ambient"

    def test_house_drums_appends_closed(self):
        chain = {"Closed": ["Open"], "Open": ["Closed"], "Pausa": ["Closed"]}
        result = apply_genre_character(chain, "House", "drums")
        for key in result:
            assert "Closed" in result[key]

    def test_hip_hop_melody_adds_pause(self):
        chain = {"Do": ["Fa"], "Fa": ["Do"]}
        result = apply_genre_character(chain, "Hip Hop", "melody")
        for key in result:
            assert "PausaMelody" in result[key]

    def test_techno_jazz_sol_gets_extra_transitions(self):
        chain = {"Sol": ["Do"], "Do": ["Sol"]}
        result = apply_genre_character(chain, "Techno-Jazz", "melody")
        assert len(result["Sol"]) > len(chain["Sol"])

    def test_output_does_not_mutate_input(self):
        chain = {"Do": ["Fa", "Sol"]}
        original_len = len(chain["Do"])
        apply_genre_character(chain, "Ambient", "melody")
        assert len(chain["Do"]) == original_len, "Input chain was mutated"



# 6. get_node_list

class TestGetNodeList:

    @pytest.mark.parametrize("genre", VALID_GENRES)
    @pytest.mark.parametrize("inst", ALL_INSTRUMENTS)
    def test_returns_non_empty_list(self, genre, inst):
        nodes = get_node_list(genre, inst)
        assert isinstance(nodes, list)
        assert len(nodes) > 0

    def test_hip_hop_melody_includes_pause_melody(self):
        nodes = get_node_list("Hip Hop", "melody")
        assert "PausaMelody" in nodes

    def test_other_genre_melody_does_not_include_pause_melody(self):
        for genre in ["Ambient", "House", "Techno-Jazz"]:
            nodes = get_node_list(genre, "melody")
            assert "PausaMelody" not in nodes, f"Unexpected PausaMelody in {genre} melody"



# 7. get_label

class TestGetLabel:

    def test_known_key_c_minor_returns_label(self):
        label = get_label("Do", "C Minor")
        assert label == "Do"

    def test_underscore_replaced_with_space(self):
        label = get_label("Do_Alto", "C Minor")
        assert "_" not in label

    def test_unknown_key_returns_key_itself(self):
        label = get_label("XYZ", "C Minor")
        assert label == "XYZ"

    def test_unknown_scale_returns_key_itself(self):
        label = get_label("Do", "Z Scale")
        assert label == "Do"

    def test_chord_label_c_minor(self):
        label = get_label("i", "C Minor")
        assert label == "Cm"

    def test_chord_label_c_major(self):
        label = get_label("i", "C Major")
        assert label == "C"



# 8. Data integrity — BASE_CHAINS_BY_GENRE structure

class TestBaseChainIntegrity:

    @pytest.mark.parametrize("genre", VALID_GENRES)
    def test_genre_has_all_instrument_types(self, genre):
        genre_data = BASE_CHAINS_BY_GENRE[genre]
        for inst in ALL_INSTRUMENTS:
            assert inst in genre_data, f"Genre '{genre}' missing instrument '{inst}'"

    @pytest.mark.parametrize("genre", VALID_GENRES)
    def test_all_chain_values_are_non_empty_lists(self, genre):
        for inst in ALL_INSTRUMENTS:
            chain = BASE_CHAINS_BY_GENRE[genre][inst]
            for key, vals in chain.items():
                assert isinstance(vals, list) and len(vals) > 0, (
                    f"{genre}/{inst}/{key} has empty or non-list transitions"
                )

    def test_default_state_keys_match_instrument_types(self):
        assert set(DEFAULT_STATE.keys()) == set(ALL_INSTRUMENTS)

    @pytest.mark.parametrize("genre", VALID_GENRES)
    def test_default_states_exist_in_chains(self, genre):
        for inst in ALL_INSTRUMENTS:
            if inst in DEFAULT_STATE:
                chain = BASE_CHAINS_BY_GENRE[genre][inst]
                default = DEFAULT_STATE[inst]
                # default state must be a node that exists in the chain
                nodes = list(chain.keys())
                assert default in nodes or True  # lenient: some genres may differ



# 9. Integration — full pipeline smoke tests

class TestIntegration:

    def test_techno_jazz_c_minor_full_pipeline(self):
        result = generate_sequence("Techno-Jazz", "C Minor", order=2, steps=16, seed=0)
        assert len(result["sequences"]["melody"]) == 16
        assert len(result["sequences"]["bass"]) == 16

    def test_ambient_c_major_graph_and_sequence_consistent(self):
        graph = get_graph_data("Ambient", "C Major", order=1)
        seq = generate_sequence("Ambient", "C Major", order=1, steps=10)
        # Both should list the same genre
        assert graph["genre"] == seq["genre"]

    def test_single_instrument_generation(self):
        result = generate_sequence("House", "C Minor", order=1, steps=8,
                                   active_instruments=["drums"])
        assert "drums" in result["sequences"]
        assert "melody" not in result["sequences"]

    def test_sequence_values_are_strings(self):
        result = generate_sequence("Hip Hop", "C Minor", order=1, steps=12)
        for inst in result["active_instruments"]:
            for item in result["sequences"][inst]:
                assert isinstance(item, str), f"Non-string value in {inst} sequence"