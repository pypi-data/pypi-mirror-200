#include "../../include/dlplan/state_space.h"


namespace dlplan::state_space {

GoalDistanceInformation::GoalDistanceInformation(
    Distances&& goal_distances,
    StateIndicesSet&& deadend_state_indices)
    : m_goal_distances(std::move(goal_distances)),
      m_deadend_state_indices(std::move(deadend_state_indices)) { }

GoalDistanceInformation::GoalDistanceInformation(const GoalDistanceInformation& other) = default;

GoalDistanceInformation& GoalDistanceInformation::operator=(const GoalDistanceInformation& other) = default;

GoalDistanceInformation::GoalDistanceInformation(GoalDistanceInformation&& other) = default;

GoalDistanceInformation& GoalDistanceInformation::operator=(GoalDistanceInformation&& other) = default;

GoalDistanceInformation::~GoalDistanceInformation() = default;

bool GoalDistanceInformation::is_goal(StateIndex state_index) const {
    auto result = m_goal_distances.find(state_index);
    if (result == m_goal_distances.end()) {
        return false;
    }
    return result->second == 0;
}

bool GoalDistanceInformation::is_nongoal(StateIndex state_index) const {
    return !is_goal(state_index);
}

bool GoalDistanceInformation::is_deadend(StateIndex state_index) const {
    return m_deadend_state_indices.count(state_index);
}

bool GoalDistanceInformation::is_alive(StateIndex state_index) const {
    return !(is_goal(state_index) || is_deadend(state_index));
}

const StateIndicesSet& GoalDistanceInformation::get_deadend_state_indices() const {
    return m_deadend_state_indices;
}

const Distances& GoalDistanceInformation::get_goal_distances() const {
    return m_goal_distances;
}

}
