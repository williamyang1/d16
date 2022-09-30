from tempfile import mkstemp
from os import fdopen,unlink,kill
import signal
from subprocess import Popen
from django.shortcuts import render, redirect,HttpResponse

def startjob(request):
    if not request.session.has_key("job"):
        outfd,outname=mkstemp()
        request.session["jobfile"]=outname
        outfile=fdopen(outfd,"a+")
        proc=Popen("python myjob.py", shell=True,stdout=outfile)
        request.session["job"]=proc.pid

        result_str='A <a href="/showjob/">new job</a> has started.'
    return HttpResponse('A <a href="/showjob/">new job</a> has started.')

def showjob(request):
    if not request.session.has_key('job'):
        return HttpResponse('Not running a job.'+\
               '<a href="/startjob/">Start a new one?</a>')
    else:
        filename=request.session["kobfile"]
        results=open(filename)
        lines=results.readlines()
        try:
            return HttpResponse(lines[-1]+\
                         '<p><a href="/rmjob/">Terminate?</a>')
        except:
            return HttpResponse('No results yet.'+\
                         '<p><a href="/rmjob/">Terminate?</a>')
    return response

def rmjob(request):
    if request.session.has_key("job"):
        job=request.session["job"]
        filename=request.session["jobfile"]
        try:
            kill(job,signal.SIGKILL)
            unlink(filename)
        except OSError as e:
            pass
        del request.session['job']
        del request.session['jobfile']



