import sys
import vtk

if len(sys.argv) != 2:
	print("Usage:", sys.argv[0], "[filename]")
	exit()

filename = sys.argv[1]

# Create a renderer
renderer = vtk.vtkRenderer()

# Read the file

generic_reader = vtk.vtkDataSetReader()
generic_reader.SetFileName(filename)
generic_reader.Update()

# create mapper
mapper = vtk.vtkDataSetMapper()

if generic_reader.GetPolyDataOutput():
	print( "Reading polydata")
	polydata = generic_reader.GetPolyDataOutput()

	# triangulation code here...

	# mapper.SetInputConnection(triangulation_filter.GetOutputPort()) 

	# set the appropriate scalar range for color mapping
	mapper.SetScalarRange(polydata.GetPointData().GetArray(0).GetRange())

elif generic_reader.GetStructuredPointsOutput():
	print("Reading Structured points")

	# set the appropriate scalar range for color mapping
	mapper.SetScalarRange(generic_reader.GetStructuredPointsOutput().GetPointData().GetArray(0).GetRange())

	mapper.SetInputConnection(generic_reader.GetOutputPort())
	
elif generic_reader.GetUnstructuredGridOutput():
	print("Reading Unstructured grid")

	# set the appropriate scalar range for color mapping
	mapper.SetScalarRange(generic_reader.GetUnstructuredGridOutput().GetPointData().GetArray(0).GetRange())

	mapper.SetInputConnection(generic_reader.GetOutputPort())

else:
	print("No reader written for this file type!")


# create actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a renderer and add the actor to the scene
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

# Create render window 
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(900, 600) # Set the window size you want
renderWindow.AddRenderer(renderer)

# Set-up interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()

# Use track-ball interaction style instead of joystick style
style =	vtk.vtkInteractorStyleTrackballCamera()

renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()

