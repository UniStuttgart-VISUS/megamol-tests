mmCreateView("test", "View3DGL", "::view")
mmCreateModule("MMPLDDataSource", "::dat")
mmCreateModule("BoundingBoxRenderer","::bbox")
mmCreateModule("DistantLight","::distlight")
mmCreateModule("SphereRenderer", "::renderer")
mmCreateCall("CallRender3DGL", "::view::rendering", "::bbox::rendering")
mmCreateCall("CallRender3DGL","::bbox::chainRendering","::renderer::rendering")
mmCreateCall("CallLight","::renderer::lights","::distlight::deployLightSlot")
mmSetParamValue("::renderer::renderMode", "Splat")
mmSetParamValue("::renderer::splat::alphaScaling", "1.000000")
mmSetParamValue("::distlight::Direction", "-0.500000;0.500000;0.000000")
mmCreateCall("MultiParticleDataCall", "::renderer::getdata", "::dat::getData")
mmSetParamValue("::view::camstore::settings", [=[{"aspect":1.7777777910232544,"direction":[-0.5251524448394775,-0.3885423541069031,-0.7571325898170471],"far_plane":16.228347778320313,"fovy":0.5,"image_plane_tile_end":[1.0,1.0],"image_plane_tile_start":[0.0,0.0],"near_plane":9.210872650146484,"position":[6.6429853439331055,4.699099063873291,9.78062629699707],"projection_type":0,"right":[0.8413097858428955,-0.10309942066669464,-0.5306299924850464],"up":[-0.1281123161315918,0.9156447649002075,-0.3810274302959442]}]=])
mmSetParamValue("::view::camstore::autoLoadSettings", "true")
mmSetParamValue("::dat::filename", [[..\tests\data\sphererenderer\test_xyz_float_rgba_float.mmpld]])
mmSetGUIVisible(false)
mmRenderNextFrame()
mmRenderNextFrame()
mmScreenshot([[result.png]])
mmQuit()
