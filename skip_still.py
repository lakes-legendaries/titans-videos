import bpy
import shutil
import os.path

def render_with_skips(start, stop):
    """
    Take start and stop, and render animation only for animated
    frames. Still frames, are substituted into the output folder
    as copies of their equivalents.
    """

    render_range = list(range(start, stop))

    # create JSON like dictionary to store each
    # animated object's fcurve data at each frame.
    all_obj_fcurves = {}
    for obj in bpy.data.objects:    
        obj_fcurves = {}

        try:
            obj.animation_data.action.fcurves
        except AttributeError:
            print("--|'%s' is not animated" % obj.name)
            continue

        print("\n--> '%s' is animated at frames:" % obj.name)

        for fr in list(range(start,stop+1)):
            fc_evals = [c.evaluate(fr) for c in obj.animation_data.action.fcurves]
            obj_fcurves.update({int(fr): fc_evals})
            print(fr, end=", ")
        print()

        all_obj_fcurves.update({obj.name: obj_fcurves})


    # loop through each animated object and find its
    # animated frames. then remove those frames from
    # a set containing all frames, to get still frames.
    still_frames = set(render_range)
    for obj in all_obj_fcurves.keys():
        obj_animated_frames = []
        for i, fr in enumerate(sorted(all_obj_fcurves[obj].keys())):
            if i != 0:
                if all_obj_fcurves[obj][fr] != all_obj_fcurves[obj][fr_prev]:
                    obj_animated_frames.append(fr)
            fr_prev = fr

        still_frames = still_frames - set(obj_animated_frames)

    print("\nFound %d still frames" % len(still_frames))
    # print(sorted(still_frames), end="\n\n")


    # render animation, skipping the still frames and
    # filling them in as copies of their equivalents
    filepath = bpy.context.scene.render.filepath
    try:
        for fr in render_range:
            
            # Get filenames
            cur_fname  = filepath + '%04d' %  fr      + '.png'
            prev_fname = filepath + '%04d' % (fr - 1) + '.png'
            
            # Skip if already exists 
            if os.path.isfile(cur_fname):
                print('Skipping ' + cur_fname)
                continue
            
            # Render if animation or prev DNE
            if fr not in still_frames or fr == render_range[0] or not os.path.isfile(prev_fname):
                
                # Set to current frame
                bpy.context.scene.frame_set(fr)
                
                # Set output file
                bpy.context.scene.render.filepath = filepath + '%04d' % fr
                print('Rendering' + bpy.context.scene.render.filepath)
                
                # Render
                bpy.ops.render.render(write_still=True)
                
                # Restore filepath
                bpy.context.scene.render.filepath = filepath
                
            # Copy previously-animated
            else:
                print('Copying Frame %04d' % fr)
                shutil.copyfile(prev_fname, cur_fname)
    except:
        # Restore filepath
        bpy.context.scene.render.filepath = filepath
            

start = bpy.data.scenes['Scene'].frame_start
end = bpy.data.scenes['Scene'].frame_end
render_with_skips(start,end)