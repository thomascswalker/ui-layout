# 1. Getting Started

## Hierarchy

GUI layouts can be thought of as a tree structure, with branches
and leaves of the tree reperesenting the various elements within a GUI.

<div style="display: flex;">
  <div style="flex: 1; padding-right: 10px;">
    
```mermaid
graph TD

A[Root] --> C1
A --> C2
C1[Frame]
C2[Text]

C1 --> C3
C1 --> C4
C1 --> C5

C3[Text]
C4[Dropdown]
C5[Button]
```

  </div>
  <div style="flex: 1; padding-left: 10px;">

![element_gui](images/element_gui.svg)

  </div>
</div>


## Elements

An element is node within the GUI tree. It is most commonly represented 
rectangularly.

![element_diagram](images/element_diagram.svg)
