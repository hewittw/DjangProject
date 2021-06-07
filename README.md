# DjangProject

I am making my own version of Reddit, aka Hewdit. It will be better! Enjoy!

First assignment commit Id number: db92952665093d414832dd6dc325168563bd5d95


# Final Version Notes

Purpose: the main point of my website/final project is to be a social media like device where the user can log in, make posts, view the posts, view profiles, and even update their own bio.

Extra 30% things: 
1) I made it so user's can create a new profile from a form
2) User's can change the data, and in turn models, by updating only their profile's bio
3) there is unlimited multi-layered commenting that uses a recursive function and can go on forever (it's pretty cool :) )

I also did some small things like getting the models to use UTC and then conveting it to LA time in the templates so that my website could hypothetically be used around the world. I also spent a fair amount of time making the UI not amazing, but pretty cool and definitely good enough to make the website usable and fun.

Another thing that took some extra time is there I have two views that have changing urls: by that I mean the urls change depending on the data that is being sent to that view. This is the case for both profile and thread, which require an id in order to have a valid url and to generate a specific view for that specific data - its far less generic than say a view like stream that just takes all the top level posts. 

Also a couple things to note:
1) I did not use all the fields in all my models because I did not have time to set everything up
2) Django has this weird error with forms, buttons, and margin spacing with a navbar - I did some research with my dad and both I and him couldn't find a fix to the problem so we hard-coded the margin and made it look the best we could.
