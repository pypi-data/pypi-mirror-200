#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // Necessary for automatic conversion of e.g. std::vectors
#include <pybind11/iostream.h>
#include <pybind11/functional.h>
#include <pybind11/embed.h> // everything needed for embedding

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#include "../../../include/dlplan/state_space.h"


namespace py = pybind11;

using namespace dlplan::core;
using namespace dlplan::state_space;


void init_state_space(py::module_ &m) {
    py::class_<GoalDistanceInformation>(m, "GoalDistanceInformation")
        .def("__copy__", [](const GoalDistanceInformation& info, py::object){ return GoalDistanceInformation(info); })
        .def("__deepcopy__", [](const GoalDistanceInformation& info, py::object){ return GoalDistanceInformation(info); })
        .def("is_goal", &GoalDistanceInformation::is_goal)
        .def("is_nongoal", &GoalDistanceInformation::is_nongoal)
        .def("is_deadend", &GoalDistanceInformation::is_deadend)
        .def("is_alive", &GoalDistanceInformation::is_alive)
        .def("get_deadend_state_indices", &GoalDistanceInformation::get_deadend_state_indices, py::return_value_policy::reference)
        .def("get_goal_distances", &GoalDistanceInformation::get_goal_distances, py::return_value_policy::reference)
    ;

    py::class_<StateInformation>(m, "StateInformation")
        .def("__copy__", [](const StateInformation& info, py::object){ return StateInformation(info); })
        .def("__deepcopy__", [](const StateInformation& info, py::object){ return StateInformation(info); })
        .def("get_state", &StateInformation::get_state, py::return_value_policy::reference)
    ;

    py::class_<StateSpace, std::shared_ptr<StateSpace>>(m, "StateSpace")
        .def(py::init<std::shared_ptr<const InstanceInfo>, StatesSet, StateIndex, AdjacencyList, StateIndicesSet>())
        .def(py::init<const StateSpace&, const StateIndicesSet&, const StateIndicesSet&>())
        .def("__copy__", [](const StateSpace& state_space, py::object){ return StateSpace(state_space); })
        .def("__deepcopy__", [](const StateSpace& state_space, py::object){ return StateSpace(state_space); })
        .def("merge", &StateSpace::operator|=)
        .def("compute_distances", &StateSpace::compute_distances)
        .def("is_goal", &StateSpace::is_goal)
        .def("is_nongoal", &StateSpace::is_nongoal)
        .def("add_state", &StateSpace::add_state, py::return_value_policy::reference)
        .def("add_transition", &StateSpace::add_transition)
        .def("print", &StateSpace::print)
        .def("to_dot", &StateSpace::to_dot)
        .def("set_initial_state_index", &StateSpace::set_initial_state_index)
        .def("set_goal_state_indices", &StateSpace::set_goal_state_indices)
        .def("compute_goal_distance_information", &StateSpace::compute_goal_distance_information)
        .def("compute_state_information", &StateSpace::compute_state_information)
        .def("get_states", &StateSpace::get_states, py::return_value_policy::reference)
        .def("get_state_indices", &StateSpace::get_state_indices, py::return_value_policy::reference)
        .def("get_num_states", &StateSpace::get_num_states)
        .def("get_initial_state_index", &StateSpace::get_initial_state_index)
        .def("get_forward_successor_state_indices", &StateSpace::get_forward_successor_state_indices, py::return_value_policy::reference)
        .def("get_backward_successor_state_indices", &StateSpace::get_backward_successor_state_indices, py::return_value_policy::reference)
        .def("get_goal_state_indices", &StateSpace::get_goal_state_indices, py::return_value_policy::reference)
        .def("get_instance_info", &StateSpace::get_instance_info)
    ;

    py::class_<StateSpaceGenerator>(m, "StateSpaceGenerator")
        .def(py::init<>())
        .def("__copy__", [](const StateSpaceGenerator& generator, py::object){ return StateSpaceGenerator(generator); })
        .def("__deepcopy__", [](const StateSpaceGenerator& generator, py::object){ return StateSpaceGenerator(generator); })
        .def("generate_state_space", [](const StateSpaceGenerator& generator, const std::string& domain_file, const std::string& instance_file){
            py::module_ state_space_generator = py::module_::import("state_space_generator.state_space_generator");
            state_space_generator.attr("generate_state_space")(domain_file, instance_file);
        })
    ;

    py::class_<StateSpaceReader>(m, "StateSpaceReader")
        .def(py::init<>())
        .def("__copy__", [](const StateSpaceReader& reader, py::object){ return StateSpaceReader(reader); })
        .def("__deepcopy__", [](const StateSpaceReader& reader, py::object){ return StateSpaceReader(reader); })
        .def("read", &StateSpaceReader::read, py::arg("vocabulary_info") = nullptr, py::arg("index") = -1)
    ;
}
