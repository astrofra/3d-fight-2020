
# Basic scene with pipeline

import harfang as hg

hg.InputInit()
hg.WindowSystemInit()

res_x, res_y = 1280, 720

win = hg.NewWindow(res_x, res_y)
hg.RenderInit(win)
hg.RenderReset(res_x, res_y, hg.ResetVSync | hg.ResetMSAA4X)

hg.AddAssetsFolder("../3d-fight_compiled/")

imgui_prg=hg.LoadProgramFromAssets('core/shader/imgui')
imgui_img_prg=hg.LoadProgramFromAssets('core/shader/imgui_image')
hg.ImGuiInit(10, imgui_prg, imgui_img_prg)

check = True
open = True
combo = 0
color = hg.Color(1, 0, 1)

# hg.SetRenderDebug(hg.RenderDebugProfiler | hg.RenderDebugStats | hg.RenderDebugText)

# Vertex model:
vs_decl = hg.VertexDecl()
vs_decl.Begin()
vs_decl.Add(hg.A_Position, 3, hg.AT_Float)
vs_decl.Add(hg.A_Normal, 3, hg.AT_Uint8, True, True)
vs_decl.End()

# Geometries models:
res = hg.PipelineResources()

cube_mdl = hg.CreateCubeModel(vs_decl, 0.5, 0.5, 0.5)
cube_ref = res.AddModel('cube', cube_mdl)
ground_size = hg.Vec3(50, 0.01, 50)
ground_mdl = hg.CreateCubeModel(vs_decl, ground_size.x, ground_size.y, ground_size.z)
ground_ref = res.AddModel('ground', ground_mdl)

# Load shader:
prg = hg.LoadPipelineProgramFromAssets('core/shader/default', 'forward')
prg_ref = res.AddProgram('default shader', prg)

# Create material
mat = hg.Material()
hg.SetMaterialProgram(mat, prg_ref)
hg.SetMaterialValue(mat, "uDiffuseColor", 0.5, 0.5, 0.5, 1)
hg.SetMaterialValue(mat, "uSpecularColor", 1, 1, 1, 0.1)

# Setup scene:
scene = hg.Scene()

# scene.SetPhysicsTimestep(1024 * 5)

cam = hg.CreateCamera(scene, hg.TransformationMat4(hg.Vec3(0, 1, -10), hg.Vec3(hg.Deg(30), 0, 0)), 0.01, 1000)

hg.LoadSceneJsonFromAssets("main.scn", scene, res, "forward")

scene.SetCurrentCamera(cam)

# rendering pipeline
pipeline = hg.CreateForwardPipeline()

# input devices and fps controller states
keyboard = hg.Keyboard()
mouse = hg.Mouse()

cam_pos = hg.Vec3(0, 1, -10)
cam_rot = hg.Vec3(0, 0, 0)

# main loop
hg.ResetClock()

while not keyboard.Down(hg.KeyEscape):
	keyboard.Update()
	mouse.Update()

	dt = hg.TickClock()

	speed = 1
	if keyboard.Down(hg.KeyLShift):
		speed = 10
	hg.FpsController(keyboard, mouse, cam_pos, cam_rot, speed, dt)

	cam.GetTransform().SetPos(cam_pos)
	cam.GetTransform().SetRot(cam_rot)

	scene.Update(dt)

	hg.SetViewClear(0, hg.ClearColor | hg.ClearDepth, 0x1f001fff, 1.0, 0)
	hg.SetViewRect(0, 0, 0, res_x, res_y)

	hg.SubmitSceneToPipeline(0, scene, hg.IntRect(0,0, res_x, res_y), True, pipeline, res)

	# imgui

	hg.ImGuiBeginFrame(res_x, res_y, dt, hg.ReadMouse(), hg.ReadKeyboard())

	if hg.ImGuiBegin("GUI"):
		_, check = hg.ImGuiCheckbox("Check", check)

		_, open = hg.ImGuiCollapsingHeader("Header", open)
		if _:
			if hg.ImGuiButton("Button"):
				print("Button pressed")

			_, combo = hg.ImGuiCombo("Combo", combo, ['item 1', 'item 2', 'item 3'])
			_, color = hg.ImGuiColorButton("Color", color)

	hg.ImGuiEnd()

	hg.ImGuiEndFrame(255)

	hg.Frame()
	hg.UpdateWindow(win)

hg.RenderShutdown()
hg.DestroyWindow(win)